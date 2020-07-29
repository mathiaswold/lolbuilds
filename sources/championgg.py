import requests
from bs4 import BeautifulSoup

from sources import Source


class Championgg(Source):

    def __init__(self):
        """ Implements champion.gg as a source """
        super().__init__("championgg")

    def get_champions(self):
        """ Gets all champions with their roles from champion.gg """
        body = requests.get("https://champion.gg/").text

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

            for role in champion_div.find_all("a"):
                if role.get("style") == "display:block":
                    champion["roles"].append(role.string.strip())

            champions.append(champion)

        return champions

    def get_items(self, champion, role):
        """ Gets the item builds (most frequent and highest win %) for a champion and role from champion.gg """

        body = requests.get(
            "https://champion.gg/champion/" + champion["name"] + "/" + role).text
        soup = BeautifulSoup(body, "html.parser")

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

        try:
            for a in soup.find("h2", string="Most Frequent Completed Build").find_next_sibling("div").find_all("a"):
                items["frequent"]["full"].append(
                    a.find("img").get("data-id"))

            for a in soup.find("h2", string="Highest Win % Starters").find_next_sibling("div").find_all("a"):
                items["highest"]["starters"].append(
                    a.find("img").get("data-id"))

            for a in soup.find("h2", string="Highest Win % Completed Build").find_next_sibling("div").find_all("a"):
                items["highest"]["full"].append(
                    a.find("img").get("data-id"))

            for a in soup.find("h2", string="Most Frequent Starters").find_next_sibling("div").find_all("a"):
                items["frequent"]["starters"].append(
                    a.find("img").get("data-id"))

        except:
            print(
                f"NOT FOUND: Build for {champion['display_name']} {role} not found on champion.gg")

        return items

    def get_skill_order(self, champion, role):
        """ Gets the recommended skill order from champion.gg """

        body = requests.get(
            "https://champion.gg/champion/" + champion["name"] + "/" + role).text
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
        """ Get current champion.gg version """
        body = requests.get("https://champion.gg/").text
        soup = BeautifulSoup(body, "html.parser")
        return soup.find("strong").text
