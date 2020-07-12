# lolbuilds

A small python script that fetches item builds from [champion.gg](https://www.champion.gg/) (most frequent and highest win %) and converts them into item sets. The items sets for every champion and role gets saved to your League of Legends installation folder, and can be used in-game. The item sets additionally shows frequent skill order used. Supports Windows and macOS.

Inspired by [Championify](https://github.com/dustinblackman/Championify).

![lolbuilds](https://i.imgur.com/4KWhcF9.png?1)

## Usage


Requires [python](https://www.python.org/downloads/) and [pip](https://pip.pypa.io/en/stable/installing/).


Download the repository, open a command prompt (cmd) / terminal and `cd` into the folder. Install required python packages with pip:

```
pip install -r requirements.txt
```

Then run `main.py`:

```
WINDOWS: py main.py
MAC: python main.py
```

**Note 1**: Due to the League of Legends' limitations, the item sets will only be available in-game, not in the client.

**Note 2**: [Champion.gg](https://www.champion.gg/) might gather game data for a week or more before builds are available to all champs and roles after a new patch.

## Specify custom League of Legends folder

You need to specify League's installation folder if it's not in the default location (Windows: "C:\Riot Games\League of Legends", macOS: "/Applications/League of Legends.app"). Do this by using the `--path` option:
```
py main.py --path <League of Legends path>
```
Example:
```
WINDOWS: py main.py --path "C:\Program Files\Riot Games\League of Legends"
MAC: python main.py --path "/Applications/League of Legends.app"
```
## Delete item sets
If you want to remove all the item sets that this script made, run this command. Remember to use the `--path` option as well if you don't have League installed in the standard location (see step above).
```
WINDOWS: py main.py --delete
MAC: python main.py --delete
```
