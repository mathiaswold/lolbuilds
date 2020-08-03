import multiprocessing
import os
import sys

from sources import SOURCES
from utils import config, versions

LOLBUILDS_VERSION = "1.2.0"


def clear():
    """ Clears the terminal """
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")


def print_script_info():
    """ Prints script title and version info """
    print("#####################")
    print("#      LoLBuilds    #")
    print(f"#       v{LOLBUILDS_VERSION}      #")
    print("#  by Mathias Wold  #")
    print("#####################")
    print()

    # check for new releases of LoLBuilds
    versions.check_lolbuilds_version(LOLBUILDS_VERSION)

    # compare local item set version to current source and LoL version to check if item sets are outdated
    current_lol_version = versions.get_lol_version()
    print(f"Current LoL version: {current_lol_version}")
    print()
    for source in SOURCES:
        versions.check_source_version(source, current_lol_version)
    print()


def update_league_path():
    """ Finds and saves the correct League of Legends path to the config """
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

    # choose between importing or deleting item sets
    answer = None

    # only accept answers "", "d" (delete) or source name
    while answer not in ["", "d"] + [source.name for source in SOURCES]:
        print()
        print("-"*36, "USAGE", "-"*36)
        print("Import:")
        print("* To import item sets from all sources, press Enter")
        for source in SOURCES:
            print(
                f"* To only import item sets from {source.name.capitalize()}, type '{source.name}' then press Enter")
        print()
        print("Delete:")
        print("* To delete item sets from one or more sources, press 'd' then Enter")
        print("-"*79)
        print()
        answer = input().lower()
    print()

    # delete items sets
    if answer.lower() == "d":
        # delete one or more item sets and exit
        clear()
        answer = None
        while answer not in ["d"] + [source.name for source in SOURCES]:
            print("* To delete item sets from all sources, type 'd' then enter")
            for source in SOURCES:
                print(
                    f"* To only delete item sets from {source.name.capitalize()}, type '{source.name}' then press Enter")
            print()
            answer = input().lower()

        # delete item sets from one specified source
        if answer.lower() in [source.name for source in SOURCES]:
            for source in SOURCES:
                if answer.lower() == source.name:
                    source.delete_item_sets()
                    break

        # delete item sets from all sources
        elif answer == "d":
        for source in SOURCES:
            source.delete_item_sets()

        # delete old item sets and import new ones from specified source
    elif answer.lower() in [source.name for source in SOURCES]:
        for source in SOURCES:
            if answer.lower() == source.name:
                source.import_item_sets()
                break

        # delete old item sets and import new ones from all sources
        # uses multiprocessing to import from multiple sources at once
    else:
        # for macos support
        if sys.platform == "darwin":
            multiprocessing.set_start_method("fork")

        p = multiprocessing.Pool(processes=min(len(SOURCES), os.cpu_count()))

        for source in SOURCES:
            p.apply_async(source.import_item_sets)

        # waits for all source imports to be done before continuing
        p.close()
        p.join()

    # last prompt before exiting the app
    print("\nDone!")
    answer = None
    while answer == None:
        answer = input("Press Enter to go back, or close this window if you want to exit")


if __name__ == "__main__":
    multiprocessing.freeze_support()
    # the line above is needed for windows multiprocessing to work in the freezed lolbuilds.exe file

    while True:
    main()
