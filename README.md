# LoLBuilds
[![GitHub Releases](https://img.shields.io/github/downloads/mathiaswold/lolbuilds/latest/total)](https://github.com/MathiasWold/lolbuilds/releases/latest)

LoLBuilds is a small python program that fetches item builds from sources such as [champion.gg](https://champion.gg/) and [probuilds.net](https://probuilds.net/) (most frequent and highest win % builds) and converts them into item sets to be used in League of Legends. LoLBuilds imports item sets for each role the champion is played in, and additionally shows the recommended skill order. Supports Windows and macOS.

Inspired by [Championify](https://github.com/dustinblackman/Championify).

![lolbuilds](https://i.imgur.com/QCK3S1f.png)


![lolbuilds](https://i.imgur.com/YRUVWNz.png?1)

## Usage

Simply run the program for your operating system (from [![GitHub Releases](https://img.shields.io/github/downloads/mathiaswold/lolbuilds/latest/total)](https://github.com/MathiasWold/lolbuilds/releases/latest)) and follow the prompts to import or delete item sets. LoLBuilds automatically searches for your League of Legends installation folder. It will ask you to specify the correct installation path if you don't have League of Legends installed in the standard location.

Sources currently implemented: [champion.gg](https://champion.gg/), [probuilds.net](https://probuilds.net) and [op.gg](https://www.op.gg/)

**Note 1**: Due to the League of Legends' limitations, the item sets will only be available in-game, not in the client.

**Note 2**: Sources might gather game data for some days before builds are available to all champs and roles after a new patch.

![lolbuilds_gif](https://i.imgur.com/dVHqWnF.gif)

## Run From Source

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

**What does this program do?**

LoLBuilds looks at all builds available at sources like champion.gg and converts them to item sets to be used in-game. This is done by creating json-files containing the builds and placing them in a specific location* in your League of Legends installation folder. The program does not touch any other League of Legends files than the json files it creates.

\* Windows example: `C:/Riot Games/League of Legends/Config/Champions/[champion]/Recommended`

**How often should i run LoLBuilds and import item sets?**

You should run LoLBuilds 3-4 days after a LoL patch comes out. A LoL patch normally comes out every two weeks. LoLBuilds tells you if any of the sources are outdated!

**Where is the config file stored?**

A folder named `.lolbuilds ` is stored in your home directory. This folder contains a single json config file.

Windows: `%userprofile%\.lolbuilds\config.json`

MacOS: `~/.lolbuilds/config.json` 

**Are the executable programs safe?**

The executable programs are created directly from the script in `main.py` using [pyinstaller](https://www.pyinstaller.org/). The script is open source and easy to look over if you so desire. If you don't trust the executables you can run the script directly from `main.py`, see ["Run From Source"](#run-from-source) above.

## [License](https://github.com/MathiasWold/lolbuilds/blob/master/LICENSE)

LoLBuilds was created under Riot Games' "Legal Jibber Jabber" policy using assets owned by Riot Games. Riot Games does not endorse or sponsor this project.
