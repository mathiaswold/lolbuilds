import argparse
import json
import os
import shutil
import sys
from sys import platform

import requests
from bs4 import BeautifulSoup


def get_champions():
    """ Gets all champions with their roles from champion.gg """
    body = requests.get("https://www.champion.gg/").text

    soup = BeautifulSoup(body, "html.parser")

    champions = []

    for champion_div in soup.find_all("div", {"class": "champ-height"}):
        champion = {
            "name": "",
            "display_name": "",
            "id": "",
            "roles": []
        }

        champion["name"] = champion_div.find(
            "div", {"class": "champ-index-img"}).get("class")[1]

        champion["display_name"] = champion_div.find(
            "span", {"class": "champion-name"}).contents[0]

        champion["id"] = champion_div.find(
            "div", {"class": "tsm-tooltip"}).get("data-id")

        # role rank is the priority of item sets in-game, the highest number is the default item set displayed in the shop
        role_rank = 10
        for role in champion_div.find_all("a"):
            if role.get("style") == "display:block":
                champion["roles"].append((role.string.strip(), role_rank))
                role_rank -= 1

        champions.append(champion)

    return champions


def get_skill_order(soup):
    """ Gets the recommended skill order from champion.gg """

    skill_order = {
        "frequent": [],
        "highest": []
    }

    for counter, skill_div in enumerate(soup.find_all("div", {"class": "skill-order"})):
        levels = skill_div.find("div", {"class": "skill"})
        q = levels.find_next_sibling("div", {"class": "skill"})
        w = q.find_next_sibling("div", {"class": "skill"})
        e = w.find_next_sibling("div", {"class": "skill"})
        r = e.find_next_sibling("div", {"class": "skill"})

        skills = {
            "q": q,
            "w": w,
            "e": e,
            "r": r
        }

        for skill, div in skills.items():
            skills[skill] = div.find(
                "div", {"class": "skill-selections"}).find("div")

        for level in range(18):
            for skill, div in skills.items():
                if div.get("class") == ["selected"]:
                    skill_order["frequent" if counter ==
                                0 else "highest"].append(skill)
                    for skill, div in skills.items():
                        skills[skill] = div.find_next_sibling("div")
                    break

    return skill_order


def format_skill_order(skill_order):
    """ 
    Formats recommended skill order into shorthand notation. 

    Example: Q.E.W.Q, Q>E>W means lv1: Q, lv2: E, lv3: W, lv4: Q, then max Q first, then E, then W. 
    """
    skills = {
        "q": 0,
        "w": 0,
        "e": 0,
    }

    output = []

    for skill in skill_order:
        if skill in skills:
            skills[skill] += 1
        for skill, count in skills.items():
            if count == 5:
                output.append(skill.upper())
                skills[skill] = 0

    first_skills = ".".join(skill_order[:4]).upper()

    try:
        return (f"{first_skills}, {output[0]}>{output[1]}>{output[2]}")
    except:
        return "Not enough data for this skill order"


def get_items_and_skill_order(champion):
    """ Gets items and skill order for every role for a champion """

    items = {}

    for role, role_rank in champion["roles"]:

        body = requests.get(
            "https://www.champion.gg/champion/" + champion["name"] + "/" + role).text
        soup = BeautifulSoup(body, "html.parser")

        role_items = {
            "rank": role_rank,
            "frequent": {
                "full": [],
                "starters": [],
                "skill_order": None
            },
            "highest": {
                "full": [],
                "starters": [],
                "skill_order": None
            }
        }

        skill_order = get_skill_order(soup)
        role_items["frequent"]["skill_order"] = skill_order["frequent"]
        role_items["highest"]["skill_order"] = skill_order["highest"]

        try:
            for a in soup.find("h2", string="Most Frequent Completed Build").find_next_sibling("div").find_all("a"):
                role_items["frequent"]["full"].append(
                    a.find("img").get("data-id"))

            for a in soup.find("h2", string="Highest Win % Starters").find_next_sibling("div").find_all("a"):
                role_items["highest"]["starters"].append(
                    a.find("img").get("data-id"))

            for a in soup.find("h2", string="Highest Win % Completed Build").find_next_sibling("div").find_all("a"):
                role_items["highest"]["full"].append(
                    a.find("img").get("data-id"))

            for a in soup.find("h2", string="Most Frequent Starters").find_next_sibling("div").find_all("a"):
                role_items["frequent"]["starters"].append(
                    a.find("img").get("data-id"))

        except:
            print(
                f"NOT FOUND: Build for {champion['display_name']} {role} not found on champion.gg")

        items[role] = role_items

    return items


def save_item_set(league_path, role, champion_name, champion_display_name, items, version):
    """ Saves an item set for a champion for a given role. """

    # standard layout for an item set
    item_set = {
        "title": f"{champion_display_name} {role} {version}",
        "type": "custom",
        "map": "any",
        "mode": "any",
        "priority": False,
        "sortrank": items["rank"],
        "champion": champion_name,
        "blocks": []  # this is where the items goes
    }

    # most frequent starter items
    frequent_starters_dict = {}
    for item_id in items["frequent"]["starters"]:
        if not item_id in frequent_starters_dict:
            frequent_starters_dict[item_id] = 1
        else:
            frequent_starters_dict[item_id] += 1

    frequent_starters = []
    for item_id, count in frequent_starters_dict.items():
        frequent_starters.append(
            {
                "count": count,
                "id": item_id
            }
        )

    # add trinket to starters
    frequent_starters.append(
        {
            "count": 1,
            "id": "3340"
        }
    )

    item_set["blocks"].append(
        {
            "items": frequent_starters,
            "type": "Most Frequent Starters"
        }
    )

    # highest win % starter items
    highest_starters_dict = {}
    for item_id in items["highest"]["starters"]:
        if not item_id in highest_starters_dict:
            highest_starters_dict[item_id] = 1
        else:
            highest_starters_dict[item_id] += 1

    highest_starters = []
    for item_id, count in highest_starters_dict.items():
        highest_starters.append(
            {
                "count": count,
                "id": item_id
            }
        )

    # add trinket to starters
    highest_starters.append(
        {
            "count": 1,
            "id": "3340"
        }
    )

    item_set["blocks"].append(
        {
            "items": highest_starters,
            "type": "Highest Win % Starters"
        }
    )

    # most frequent full build
    frequent_full_dict = {}
    for item_id in items["frequent"]["full"]:
        if not item_id in frequent_full_dict:
            frequent_full_dict[item_id] = 1
        else:
            frequent_full_dict[item_id] += 1

    frequent_full = []
    for item_id, count in frequent_full_dict.items():
        frequent_full.append(
            {
                "count": count,
                "id": item_id
            }
        )

    item_set["blocks"].append(
        {
            "items": frequent_full,
            "type": "Most Frequent Build"
        }
    )

    # highest win % full build
    highest_full_dict = {}
    for item_id in items["highest"]["full"]:
        if not item_id in highest_full_dict:
            highest_full_dict[item_id] = 1
        else:
            highest_full_dict[item_id] += 1

    highest_full = []
    for item_id, count in highest_full_dict.items():
        highest_full.append(
            {
                "count": count,
                "id": item_id
            }
        )

    item_set["blocks"].append(
        {
            "items": highest_full,
            "type": "Highest Win % Build"
        }
    )

    # add consumables with most frequent skill order in description
    item_set["blocks"].append(
        {
            "items": [
                {
                    "count": 1,
                    "id": "2003"
                },
                {
                    "count": 1,
                    "id": "2031"
                },
                {
                    "count": 1,
                    "id": "2055"
                },
                {
                    "count": 1,
                    "id": "2138"
                },
                {
                    "count": 1,
                    "id": "2139"
                },
                {
                    "count": 1,
                    "id": "2140"
                }
            ],
            "type": "Consumables | Frequent: " + format_skill_order(items["frequent"]["skill_order"])
        }
    )

    # add trinkets with highest win % skill order in description
    item_set["blocks"].append(
        {
            "items": [
                {
                    "count": 1,
                    "id": "3340"
                },
                {
                    "count": 1,
                    "id": "3363"
                },
                {
                    "count": 1,
                    "id": "3364"
                }
            ],
            "type": "Trinkets | Wins: " + format_skill_order(items["highest"]["skill_order"])
        }
    )

    # save the item set
    champ_path = os.path.join(
        league_path, f"Config/Champions/{champion_name}/Recommended")

    # champion folders are not made by default on MacOS
    try:
        os.makedirs(champ_path)
    except FileExistsError:
        pass

    item_set_path = os.path.join(champ_path, f"ChampionGG_{role}.json")

    with open(item_set_path, "w") as f:
        f.write(json.dumps(item_set))


def delete_item_sets(league_path):
    """ Deletes all item sets generated by this script """
    champions = get_champions()

    for champion in champions:
        try:
            champ_path = os.path.join(
                league_path, f"Config/Champions/{champion['name']}/Recommended")
            item_sets = os.listdir(champ_path)
            for item_set in item_sets:
                if "ChampionGG_" in item_set:
                    os.remove(os.path.join(champ_path, item_set))
        except:
            continue


def get_lol_version():
    """ Get current League of Legends version """
    versions = json.loads(requests.get(
        "https://ddragon.leagueoflegends.com/api/versions.json").text)
    # reformats from 10.14.5 to 10.14
    latest = ".".join(versions[0].split(".")[:2])
    return latest


def get_championgg_version():
    """ Get current champion.gg version """
    body = requests.get("https://www.champion.gg/").text
    soup = BeautifulSoup(body, "html.parser")
    return soup.find("strong").text


def get_from_config(key):
    """ Get value from key in config """
    home_path = os.path.expanduser("~")

    if os.path.isfile(os.path.join(home_path, ".lolbuilds", "config.json")):
        # if config is made
        with open(os.path.join(home_path, ".lolbuilds", "config.json")) as f:
            config = json.load(f)
    else:
        # return standard values
        config = {
            "path": None,
            "local_item_version": None
        }
    return config[key]


def save_to_config(key, value):
    """ Save a (key, value) pair to the local config file in ~/.lolbuilds/config.json """
    home_path = os.path.expanduser("~")

    try:
        os.makedirs(os.path.join(home_path, ".lolbuilds"))

    except FileExistsError:
        # config already exists
        with open(os.path.join(home_path, ".lolbuilds", "config.json"), "r") as f:
            config = json.load(f)
            config[key] = value

        with open(os.path.join(home_path, ".lolbuilds", "config.json"), "w") as f:
            f.write(json.dumps(config))

    else:
        # config is created for the first time
        with open(os.path.join(home_path, ".lolbuilds", "config.json"), "w") as f:
            config = {
                "path": None,
                "local_item_version": None
            }
            config[key] = value
            f.write(json.dumps(config))


def print_script_info():
    """ Prints script title and version info """
    print("#####################")
    print("#      lolbuilds    #")
    print("#       v1.0.0      #")
    print("#  by Mathias Wold  #")
    print("#####################")
    print()

    # compare local item set version to current champion.gg and LoL version
    current_lol_version = get_lol_version()
    championgg_version = get_championgg_version()
    local_version = get_from_config('local_item_version')

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


def clear():
    """ Clears the terminal """
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")


def main():
    """ Main program that deals with user input """
    clear()
    print_script_info()

    # standard League of Legends folder location for macOS / Windows
    if platform == "darwin":
        league_path = "/Applications/League of Legends.app"
        macos = True
    elif platform == "win32":
        league_path = "C:\Riot Games\League of Legends"
        macos = False
    else:
        # Exit if used on another platform than macOS / Windows
        raise SystemExit("Operating system not supported.")

    print(f"Detected operating system: {'MacOS' if macos else 'Windows'}")

    home_path = os.path.expanduser("~")

    # check if a custom path is already saved in ~/.lolbuilds/config.json
    saved_path = get_from_config("path")
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

        # save the custom path in a config file in ~/.lolbuilds/config.json
        save_to_config("path", league_path)

        clear()
        print_script_info()
        print(f"Detected operating system: {'MacOS' if macos else 'Windows'}")

    print(f"Found League of Legends at {league_path}")

    # league folder structure is different on macos
    if macos:
        league_path = os.path.join(league_path, "Contents/LoL")

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
        save_to_config("local_item_version", None)
        delete_item_sets(league_path)

    else:
        # delete old item sets and import new ones from champion.gg
        print("Deleting old item sets...")
        delete_item_sets(league_path)

        championgg_version = get_championgg_version()
        save_to_config("local_item_version", championgg_version)

        champions = get_champions()
        for champion in champions:
            print(
                f"Adding {champion['display_name']}'s item sets...", end="\r")

            all_items = get_items_and_skill_order(champion)
            for role, items in all_items.items():
                save_item_set(league_path, role,
                              champion["name"], champion["display_name"], items, championgg_version)

            print(" "*80, end="\r")

    # last prompt before exiting the app
    print("Done!")
    answer = None
    while answer == None:
        answer = input("Press Enter to exit")


if __name__ == "__main__":
    main()
