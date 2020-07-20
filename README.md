# lolbuilds

A small python script that fetches item builds from [champion.gg](https://www.champion.gg/) (most frequent and highest win %) and converts them into item sets. The items sets for every champion and role gets saved to your League of Legends installation folder, and can be used in-game. The item sets additionally shows recommended skill order. Supports Windows and macOS.

Inspired by [Championify](https://github.com/dustinblackman/Championify).

![lolbuilds](https://i.imgur.com/60QabgT.png?1)


## Usage

Simply run the executable program for your operating system (see releases) and follow the prompts to import or delete item sets. The script automatically searches for your League of Legends installation folder. It will ask you to specify the correct path if you don't have League installed in the standard location.

**Note 1**: Due to the League of Legends' limitations, the item sets will only be available in-game, not in the client.

**Note 2**: [Champion.gg](https://www.champion.gg/) might gather game data for a week or more before builds are available to all champs and roles after a new patch.


## Run script without executables

You can also run the script manually without using the executables.
Requires [python](https://www.python.org/downloads/) and [pip](https://pip.pypa.io/en/stable/installing/).


Download the repository, open a command prompt (cmd) / terminal and `cd` into the folder. Install required python packages with pip:

```
pip install -r requirements.txt
```

Then run `main.py` and follow the prompts:

```
WINDOWS: py main.py
MAC: python main.py
```

## FAQ

**What does this script do?**

The script looks at all builds available at champion.gg and converts them to item sets to be used in game. This is done by creating json-files containing the builds and placing them in a specific location in your League of Legends installation folder. The script does not touch any other League of Legends files than the json files it creates.


**Where is the config file stored?**

A folder named `.lolbuilds ` is stored in your home directory. This folder contains a single json config file.

Windows: `%userprofile%\.lolbuilds\config.json`

MacOS: `~/.lolbuilds/config.json` 

**Are the executable programs safe?**

The executables are created directly from the script in `main.py` using [pyinstaller](https://www.pyinstaller.org/). The script is open source and easy to look over if you so desire. If you dont trust the executables you can run the script directly from `main.py`, info [here](#run-script-without-executables).

## [License](https://github.com/MathiasWold/lolbuilds/blob/master/LICENSE)

lolbuilds was created under Riot Games' "Legal Jibber Jabber" policy using assets owned by Riot Games.  Riot Games does not endorse or sponsor this project.