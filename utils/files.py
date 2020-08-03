import json
import os

from utils import config


def _format_skill_order(skill_order):
    """ 
    Formats recommended skill order into shorthand notation. 

    Output example: "Q.E.W.Q, Q>E>W" means lv1: Q, lv2: E, lv3: W, lv4: Q, then max Q first, then E, then W. 
    """
    skills = {
        "q": 0,
        "w": 0,
        "e": 0,
    }

    shorthand = []

    for skill in skill_order:
        skill = skill.lower()
        if skill in skills:
            skills[skill] += 1
        for skill, count in skills.items():
            if count == 5:
                shorthand.append(skill.upper())
                skills[skill] = 0

    for key in ["q", "w", "e"]:
        if skills[key] == 0:
            del skills[key]

    # in case of skill_order with fewer than 18 skills
    if len(skills) > 0:
        shorthand_list = sorted(
            skills.items(), key=lambda e: e[1], reverse=True)
        for skill in shorthand_list:
            shorthand.append(skill[0].upper())

    try:
        # shorthand format: Q>E>W
        shorthand = f"{shorthand[0]}>{shorthand[1]}>{shorthand[2]}"
        # first skills format: Q.E.W.Q
        first_skills = ".".join(skill_order[:4]).upper()
        return (f"{first_skills}, {shorthand}")

    except:
        return "Not enough data for this skill order"


def save(champion, item_set, version, source_name, roles):
    """ Saves an item set for a champion for a given role. """

    # standard layout for an item set
    output = {
        "title": f"{source_name.capitalize()}{(' ' + item_set['role']) if roles else ''} {version}",
        "type": "custom",
        "map": "any",
        "mode": "any",
        "priority": False,
        "champion": champion["name"],
        "blocks": []  # this is where the items goes
    }

    # add sort_rank if roles are supported, higher sort rank equals higher position in the item set list in-game
    if roles:
        output["sortrank"] = item_set["sort_rank"]

    # most frequent starter items
    frequent_starters_dict = {}
    for item_id in item_set["frequent"]["starters"]:
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

    output["blocks"].append(
        {
            "items": frequent_starters,
            "type": "Most Frequent Starters"
        }
    )

    # highest win % starter items
    highest_starters_dict = {}
    for item_id in item_set["highest"]["starters"]:
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

    output["blocks"].append(
        {
            "items": highest_starters,
            "type": "Highest Win % Starters"
        }
    )

    # most frequent full build
    frequent_full_dict = {}
    for item_id in item_set["frequent"]["full"]:
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

    output["blocks"].append(
        {
            "items": frequent_full,
            "type": "Most Frequent Build"
        }
    )

    # highest win % full build
    highest_full_dict = {}
    for item_id in item_set["highest"]["full"]:
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

    output["blocks"].append(
        {
            "items": highest_full,
            "type": "Highest Win % Build"
        }
    )

    # add consumables with most frequent skill order in description
    output["blocks"].append(
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
            "type": "Consumables | Frequent: " + _format_skill_order(item_set["frequent"]["skill_order"])
        }
    )

    # add trinkets with highest win % skill order in description
    output["blocks"].append(
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
            "type": "Trinkets | Wins: " + _format_skill_order(item_set["highest"]["skill_order"])
        }
    )

    # save the item set
    champion_path = os.path.join(
        config.get("path"), f"Config/Champions/{champion['name']}/Recommended")

    # champion folders are not made by default on MacOS
    try:
        os.makedirs(champion_path)
    except FileExistsError:
        pass

    # example file name: championgg_Top.json
    file_name = source_name
    if roles:
        file_name += "_" + item_set['role']

    item_set_path = os.path.join(
        champion_path, f"{file_name}.json")

    with open(item_set_path, "w") as f:
        f.write(json.dumps(output))


def delete(champion, source_name):
    """ Deletes item sets for a champion generated by a source. """

    try:
        champ_path = os.path.join(
            config.get("path"), f"Config/Champions/{champion['name']}/Recommended")
        item_sets = os.listdir(champ_path)
        for item_set in item_sets:
            if source_name in item_set:
                os.remove(os.path.join(champ_path, item_set))
    except FileNotFoundError:
        pass
