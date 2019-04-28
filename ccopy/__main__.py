import argparse
# import configparser
import sys

from .db import CharacterCopier


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--conf', dest='conf', help='Path to mangosd.conf')
    parser.add_argument('src', help='Name of character to copy.')
    parser.add_argument('dst', help='Name for the copied character.')

    args = parser.parse_args()

    # Apparently this ships with duplicate values by default which blows
    # up the config parser, so parse it manually
    # config = configparser.ConfigParser(strict=False)
    # config.read(args.conf)

    with open(args.conf, 'r') as f:
        conf = f.read()

        start = 0
        while start >= 0:
            start = conf.find('CharacterDatabase.Info', start)
            end = conf.find('\n', start)
            try:
                _, credentials = conf[start:end].split('=')
                break
            except ValueError:
                start += 1
                continue
        else:
            print("Can't parse config file. Exiting.")
            sys.exit(1)

        credentials = credentials.strip().replace('"', '')

    host, port, user, passwd, db = credentials.split(';')

    copier = CharacterCopier(args.src, args.dst, user, passwd, host, port, db)
    copier.run()


if __name__ == '__main__':
    main()
