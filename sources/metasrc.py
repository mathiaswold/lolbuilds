import requests
from bs4 import BeautifulSoup

from . import Source


class Metasrc(Source):

    def __init__(self):
        """ Implements champion.gg as a source """
        super().__init__("metasrc")

    def get_champions(self):
        """ Gets all champions with their roles from champion.gg """
        body = requests.get(
            "https://www.metasrc.com/5v5?ranks=platinum,diamond,master,grandmaster,challenger").text

        soup = BeautifulSoup(body, "html.parser")

        champions = []

        for champion_div in soup.find_all("div", {"class": "champion-grid-item"}):
            champion = {
                "name": "",
                "display_name": "",
                "id": "",
                "roles": []
            }

            champion["name"] = champion_div.get(
                "data-search-terms-like").split("|")[1]

            champion["display_name"] = champion_div.get(
                "data-search-terms-like").split("|")[0]

            main_role = champion_div.get(
                "data-search-terms-exact").split("|")[0]
            champion["roles"].append(main_role)

            champions.append(champion)

        return champions

    def get_items(self, champion, role):
        """ Gets the item builds (most frequent and highest win %) for a champion and role from champion.gg """
        print(f"https://www.metasrc.com/5v5/champion/{champion['name']}/{role}?ranks=platinum,diamond,master,grandmaster,challenger")
        body = requests.get(f"https://www.metasrc.com/5v5/champion/{champion['name']}/{role}?ranks=platinum,diamond,master,grandmaster,challenger").text
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

        for counter, starters in enumerate(soup.find_all("div", {"class": "_iqcim1"})):
            for item in starters.find_all("img", {"class": "lozad"}):
                if counter == 0:
                    if item.get("alt") != "coin":
                        items["frequent"]["starters"].append(item.get("data-src").split("item")[1][1:5])
                        items["frequent"]["starters"] = list(dict.fromkeys(items["frequent"]["starters"]))
                else:
                    if item.get("alt") != "coin":
                        items["highest"]["starters"].append(item.get("data-src").split("item")[1][1:5])
                        items["highest"]["starters"] = list(dict.fromkeys(items["highest"]["starters"]))
        
        print(len(soup.find("div", {"class": "_sfh2p9-3"}).contents))

        # for item_div in soup.find("div", {"class": "_sfh2p9-3"}).contents[0].contents:
            # print("-----------------")
            # item = item_div.find("img", {"class": "lozad"})
            # items["frequent"]["full"].append(item.get("data-src").split("item")[1][1:5])

        print(items)

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
