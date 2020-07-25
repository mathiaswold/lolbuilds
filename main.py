import os
import sys

from sources import championgg
from utils import config, files, versions


def clear():
    """ Clears the terminal """
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")


def print_script_info():
    """ Prints script title and version info """
    print("#####################")
    print("#      lolbuilds    #")
    print("#       v1.0.0      #")
    print("#  by Mathias Wold  #")
    print("#####################")
    print()

    # compare local item set version to current champion.gg and LoL version
    current_lol_version = versions.get_lol_version()
    championgg_version = championgg.get_version()
    local_version = config.get("ChampionGG")

    championgg_outdated = ""
    if float(current_lol_version) > float(championgg_version):
        championgg_outdated = "(Not updated to new patch yet)"

    local_outdated = ""
    if local_version is not None:
        if float(championgg_version) > float(local_version):
            local_outdated = "(outdated!)"

    print(f"Current LoL version: {current_lol_version}")
    print(
        f"Current champion.gg version: {championgg_version} {championgg_outdated}")
    print(f"Local item set version: {local_version} {local_outdated}")
    print()


def update_league_path():
    # standard League of Legends folder location for macOS / Windows
    if sys.platform == "darwin":
        league_path = "/Applications/League of Legends.app/Contents/LoL"
        macos = True
    elif sys.platform == "win32":
        league_path = "C:\Riot Games\League of Legends"
        macos = False
    else:
        # Exit if used on another platform than macOS / Windows
        raise SystemExit("Operating system not supported.")

    # check if a custom path is already saved in ~/.lolbuilds/config.json
    saved_path = config.get("path")
    if saved_path is not None:
        league_path = saved_path

    # ask for a custom path if standard path is incorrect
    if not os.path.isdir(league_path):
        windows_path = "C:\Program Files\Riot Games\League of Legends"
        mac_path = "/Applications/League of Legends.app"
        print(
            f"Can't find the League of Legends folder at the standard location ({league_path})")
        print("Please type or paste the correct League of Legends path.")
        print(f"Example: { mac_path if macos else windows_path }")
        print()

        league_path = input()
        while not os.path.isdir(league_path) or "league of legends" not in league_path.lower():
            print("Please point to the League of Legends folder/app")
            print(f"Example: { mac_path if macos else windows_path }")
            league_path = input()

        clear()
        print_script_info()

        # open app content on macOS
        if macos:
            league_path = os.path.join(league_path, "Contents/LoL")

    # save the path in a config file in ~/.lolbuilds/config.json
    config.save("path", league_path)

    print(f"Found League of Legends at {league_path}")


def main():
    """ Main program that deals with user input """
    clear()
    print_script_info()

    update_league_path()

    # choose between importing and deleting the item sets
    answer = None
    while answer not in ["", "d"]:
        print()
        print("To import item sets, press Enter")
        print("To delete item sets, press 'd' then Enter")
        print()
        answer = input()
    print()

    if answer.lower() == "d":
        # delete all item sets and exit
        print("Deleting item sets...")
        config.save("local_item_version", None)
        files.delete_all()

    else:
        # delete old item sets and import new ones from champion.gg
        print("Deleting old item sets...")
        files.delete_all()

        championgg.import_item_sets()

    # last prompt before exiting the app
    print("Done!")
    answer = None
    while answer == None:
        answer = input("Press Enter to exit")


if __name__ == "__main__":
    main()
