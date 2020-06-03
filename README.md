# lolbuilds

A small python script that fetches item builds from [champion.gg](https://www.champion.gg/) (most frequent and highest win %) and converts them into item sets. The items sets for every champion and role gets saved to your League of Legends installation folder, and can be used in-game. The item sets additionally shows frequent skill order used. Currently for Windows only.

Inspired by [Championify](https://github.com/dustinblackman/Championify).

## Usage

---
**Warning**: There script currently does not support removing the item sets. This means you have to delete the JSON files with the item sets for each champions manually from the installation folder. Use at own risk.

---
Requires [python](https://www.python.org/downloads/) and [pip](https://pip.pypa.io/en/stable/installing/).


Download the repository, open a command prompt (cmd) and `cd` into the folder. Install required python packages with pip:

```
pip install -r requirements.txt
```

Then run `main.py`:

```
py main.py
```

**Note 1**: The python script assumes you have League of Legends installed in `C:/Riot Games/League of Legends/`. If you have the game installed in another folder you need to change variable `riot_path` on line 313 in `main.py` to the correct file path. 

**Note 2**: Due to the League of Legends' limitations, the item sets will only be available in-game, not in the client.
