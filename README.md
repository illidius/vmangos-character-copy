This is a tool for creating character copies on LightsHope databases. It has
not been extensively tested so I would recommend backing up your database
before using this, just in case.

# Requirements

I assume you're running [vmangos](https://github.com/vmangos/core) or an
equivalent lightshope core repack. You also need to have Python 3.5 or later.

On ubuntu/debian distros:
```bash
sudo apt install python3 python3-pip
```

On Windows:
[Python Downloads](https://www.python.org/downloads/). Grab the latest
(3.7.3 at the time of this writing), and make sure you keep `pip` checked
under Optional Features when installing.

# Installation

Linux:

```bash
sudo python3 setup.py install
```

Windows:

Run a cmd or powershell as admin:
```bash
python setup.py install
```

# Usage:

From a terminal (or cmd/powershell on Windows):

```bash
ccopy --conf <</path/to/mangosd.conf>> <<Source character name>> <<Destination character name>>
```
