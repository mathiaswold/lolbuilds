from datetime import date

import requests
from bs4 import BeautifulSoup

from sources import Source


class Probuilds(Source):

    def __init__(self):
        """ Implements probuilds.net as a source """
        super().__init__("probuilds", False)

    def get_champions(self):
        """ Gets all champions from probuilds.net """

        response = requests.get(
            "https://www.probuilds.net/ajax/championListNew")

        response = response.json()["champions"]

        champions = []

        for champion_dict in response:

            champion = {
                "name": champion_dict["id"],
                "display_name": champion_dict["name"],
                "id": champion_dict["key"],
            }

            champions.append(champion)

        return champions

    def get_items(self, champion):
        """ Gets the item builds (most frequent and highest win %) for a champion from probuilds """

        items = {
            "frequent": {
                "full": [],
                "starters": [],
            },
            "highest": {
                "full": [],
                "starters": [],
            }
        }

        # get highest KDA winning build
        response = requests.get(
            f"https://www.probuilds.net/ajax/champBuilds?championId={champion['id']}")

        response = response.json()

        matches = response["matches"]
        build_order = response["buildOrder"]

        builds = []

        for match in matches:

            match_soup = BeautifulSoup(match, "html.parser")

            kda_div = match_soup.find("div", {"class": "kda"})
            kills = int(kda_div.find("span", {"class": "green"}).contents[0])
            deaths = int(kda_div.find("span", {"class": "red"}).contents[0])
            assists = int(kda_div.find("span", {"class": "gold"}).contents[0])

            kda = (kills + assists) / (1 if deaths == 0 else deaths)

            build_div = match_soup.find("div", {"class": "items"})

            # remove trinket from build
            item_divs = build_div.find_all("img", {"class": "tooltip"})[:-1]

            build = []

            for item_div in item_divs:
                build.append(item_div.get("data-id"))

            builds.append((build, kda))

        # sort by KDA
        builds.sort(key=lambda match: match[1], reverse=True)

        # not enough data for build
        try:
            items["highest"]["full"] = builds[0][0]
        except IndexError:
            print(
                f"NOT FOUND: Highest win % build for {champion['display_name']} not found on probuilds.net")

        # getting starter items
        build_order_soup = BeautifulSoup(build_order, "html.parser")
        build_order_items = build_order_soup.find(
            "div", {"class": "build-list"})

        try:
            # digging through bad html
            starter_item_1 = build_order_items.contents[1]
            starter_item_2 = starter_item_1.contents[1]
            starter_item_3 = starter_item_1.contents[3]  # might be None

            for starter_item in [starter_item_1, starter_item_2, starter_item_3]:
                data_id = starter_item.get("data-id")

                # don't include None and trinkets in starter items
                if data_id is not None and data_id != "3340":
                    items["highest"]["starters"].append(data_id)

            items["frequent"]["starters"] = items["highest"]["starters"]
        except IndexError:
            print(
                f"NOT FOUND: Starter items for {champion['display_name']} not found on probuilds.net")

        # get frequent build
        response = requests.get(
            f"https://www.probuilds.net/champions/details/{champion['id']}")
        html = response.text

        frequent_soup = BeautifulSoup(html, "html.parser")

        frequent_items_div = frequent_soup.find(
            "div", {"class": "popular-section"})

        for item_div in frequent_items_div.find_all("div", {"class": "bigData"}):
            data_id = item_div.find("div", {"class": "tooltip"}).get("data-id")
            items["frequent"]["full"].append(data_id)

        # not enough data for build
        if len(items["frequent"]["full"]) == 0:
            print(
                f"NOT FOUND: Frequent build for {champion['display_name']} not found on probuilds.net")

        return items

    def get_skill_order(self, champion):
        """ Gets the recommended skill order from champion.gg """
        # TODO: Parse skill order from probuilds

        body = requests.get(
            "https://champion.gg/champion/" + champion["name"]).text
        soup = BeautifulSoup(body, "html.parser")

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

    def get_version(self):
        """ Get current probuild version """
        # returns date because probuilds does not have a verison number listed
        return str(date.today())
