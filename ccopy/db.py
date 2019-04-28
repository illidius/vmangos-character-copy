from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy.orm.session import make_transient
from sqlalchemy import create_engine, func


class CharacterCopier:
    def __init__(self, src, dst, user, passwd, host, port, db):
        self.src = src
        self.dst = dst

        url = (
            'mysql+mysqldb://'
            + user
            + ':' + passwd
            + '@' + host
            + ':' + port
            + '/' + db
        )

        self.engine = create_engine(url)
        base = automap_base()
        base.prepare(self.engine, reflect=True)

        self.classes = base.classes

    def run(self):
        characters = self.classes.characters
        character_action = self.classes.character_action
        character_homebind = self.classes.character_homebind

        character_inventory = self.classes.character_inventory
        character_pet = self.classes.character_pet
        character_queststatus = self.classes.character_queststatus
        character_reputation = self.classes.character_reputation
        character_skills = self.classes.character_skills
        character_social = self.classes.character_social
        character_spell = self.classes.character_spell
        character_spell_cooldown = self.classes.character_spell_cooldown
        character_stats = self.classes.character_stats

        item_instance = self.classes.item_instance

        pet_spell = self.classes.pet_spell
        pet_spell_cooldown = self.classes.pet_spell_cooldown

        session = Session(self.engine)

        item_guid = session.query(func.max(item_instance.guid)).scalar() + 1
        character_guid = session.query(func.max(characters.guid)).scalar() + 1
        pet_id = session.query(func.max(character_pet.id)).scalar() + 1

        character = (
            session
            .query(characters)
            .filter(characters.name.in_([self.src]))
            .all()
        )

        assert len(character) == 1
        character = character[0]

        homebind = (
            session
            .query(character_homebind)
            .filter(character_homebind.guid.in_([character.guid]))
            .all()
        )

        assert len(homebind) == 1
        homebind = homebind[0]
        session.expunge(homebind)
        make_transient(homebind)
        homebind.guid = character_guid

        items = (
            session
            .query(item_instance)
            .filter(item_instance.owner_guid.in_([character.guid]))
            .all()
        )

        item_map = {}

        for i, item in enumerate(items):
            session.expunge(item)
            make_transient(item)
            new_guid = item_guid + i
            item_map[item.guid] = new_guid
            item.guid = new_guid
            item.owner_guid = character_guid

        actions = (
            session
            .query(character_action)
            .filter(character_action.guid.in_([character.guid]))
            .all()
        )

        for action in actions:
            session.expunge(action)
            make_transient(action)
            action.guid = character_guid

        inventory = (
            session
            .query(character_inventory)
            .filter(character_inventory.guid.in_([character.guid]))
            .all()
        )

        for element in inventory:
            session.expunge(element)
            make_transient(element)
            element.guid = character_guid
            element.item = item_map[element.item]

        pets = (
            session
            .query(character_pet)
            .filter(character_pet.owner.in_([character.guid]))
            .all()
        )

        pet_map = {}

        for i, pet in enumerate(pets):
            session.expunge(pet)
            make_transient(pet)
            new_id = pet_id + i
            pet_map[pet.id] = new_id
            pet.id = new_id
            pet.owner = character_guid

        quests = (
            session
            .query(character_queststatus)
            .filter(character_queststatus.guid.in_([character.guid]))
            .all()
        )

        for quest in quests:
            session.expunge(quest)
            make_transient(quest)
            quest.guid = character_guid

        reputation = (
            session
            .query(character_reputation)
            .filter(character_reputation.guid.in_([character.guid]))
            .all()
        )

        for rep in reputation:
            session.expunge(rep)
            make_transient(rep)
            rep.guid = character_guid

        skills = (
            session
            .query(character_skills)
            .filter(character_skills.guid.in_([character.guid]))
            .all()
        )

        for skill in skills:
            session.expunge(skill)
            make_transient(skill)
            skill.guid = character_guid

        social = (
            session
            .query(character_social)
            .filter(character_social.guid.in_([character.guid]))
            .all()
        )

        for friend in social:
            session.expunge(friend)
            make_transient(friend)
            friend.guid = character_guid

        spells = (
            session
            .query(character_spell)
            .filter(character_spell.guid.in_([character.guid]))
            .all()
        )

        for spell in spells:
            session.expunge(spell)
            make_transient(spell)
            spell.guid = character_guid

        spell_cds = (
            session
            .query(character_spell_cooldown)
            .filter(character_spell_cooldown.guid.in_([character.guid]))
            .all()
        )

        for spell_cd in spell_cds:
            session.expunge(spell_cd)
            make_transient(spell_cd)
            spell_cd.guid = character_guid

        stats = (
            session
            .query(character_stats)
            .filter(character_stats.guid.in_([character.guid]))
            .all()
        )

        for stat in stats:
            session.expunge(stat)
            make_transient(stat)
            stat.guid = character_guid

        pet_spells = (
            session
            .query(pet_spell)
            .filter(pet_spell.guid.in_(list(pet_map.keys())))
            .all()
        )

        for spell in pet_spells:
            session.expunge(spell)
            make_transient(spell)
            new_guid = pet_map[spell.guid]
            spell.guid = new_guid

        pet_spell_cds = (
            session
            .query(pet_spell_cooldown)
            .filter(pet_spell_cooldown.guid.in_(list(pet_map.keys())))
            .all()
        )

        for spell_cd in pet_spell_cds:
            session.expunge(spell_cd)
            make_transient(spell_cd)
            new_guid = pet_map[spell_cd.guid]
            spell_cd.guid = new_guid

        session.expunge(character)
        make_transient(character)

        character.guid = character_guid
        character.name = self.dst

        session.add_all(items)
        session.add_all(actions)
        session.add_all(inventory)
        session.add_all(pets)
        session.add_all(quests)
        session.add_all(reputation)
        session.add_all(skills)
        session.add_all(social)
        session.add_all(spells)
        session.add_all(spell_cds)
        session.add_all(stats)
        session.add_all(pet_spells)
        session.add_all(pet_spell_cds)
        session.add(homebind)
        session.add(character)

        session.commit()

