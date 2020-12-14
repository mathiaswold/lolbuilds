import requests
from bs4 import BeautifulSoup

from sources import Source


class Opgg(Source):

    def __init__(self):
        """ Implements op.gg as a source """
        super().__init__("opgg")

    def get_champions(self):
        html = requests.get("https://euw.op.gg/champion/statistics").text
        soup = BeautifulSoup(html, "html.parser")
        all_champion_divs = soup.find(
            "div", {"class": "champion-index__champion-list"}).find_all("div", {"class": "champion-index__champion-item"})

        champions = []

        for champion_div in all_champion_divs:

            champion = {
                "name": "",
                "display_name": "",
                "roles": []
            }

            champion["name"] = champion_div.get("data-champion-key")
            try:
                champion["display_name"] = champion_div.find("a").find(
                    "div", {"class": "champion-index__champion-item__name"}).text
            except:
                # champion doesn't have enough data and thus no stats --> skip
                continue

            for role_div in champion_div.find("a").find_all("div", {"class": "champion-index__champion-item__position"}):

                role = role_div.find("span").text

                if role.lower() == "middle":
                    champion["roles"].append("Mid")
                elif role.lower() == "bottom":
                    champion["roles"].append("Bot")
                else:
                    champion["roles"].append(role)

            champions.append(champion)

        return champions

    def get_items(self, champion, role):
        html = requests.get(
            f"https://euw.op.gg/champion/{champion['name']}/statistics/{role.lower()}/item").text
        soup = BeautifulSoup(html, "html.parser")

        tables = soup.find_all("table", {"class": "champion-stats__table"})

        core_builds = []
        core_rows = tables[0].find_all("tr")[1:]
        for row in core_rows:
            items = []
            items_td = row.find(
                "td", {"class": "champion-stats__table__cell--data"})
            for item in items_td.find_all("li", {"class": "champion-stats__list__item"}):
                items.append(item.find("img").get("src").split("item")[1][1:5])
            pick_rate = float(row.find("td", {
                              "class": "champion-stats__table__cell--pickrate"}).text.strip().split("%")[0])
            win_rate = float(row.find("td", {
                             "class": "champion-stats__table__cell--winrate"}).text.strip().split("%")[0])
            core_builds.append((items, pick_rate, win_rate))

        # choose core build with highest pick rate
        frequent_core = sorted(
            core_builds, key=lambda e: e[1], reverse=True)[0][0]

        # choose core build with highest win rate
        highest_core = sorted(
            core_builds, key=lambda e: e[2], reverse=True)[0][0]

        boots = []
        boots_rows = tables[1].find_all("tr")[1:]
        for row in boots_rows:
            item_div = row.find(
                "div", {"class": "champion-stats__single__item"})
            boots_id = item_div.find("img").get("src").split("item")[1][1:5]
            pick_rate = float(row.find("td", {
                              "class": "champion-stats__table__cell--pickrate"}).text.strip().split("%")[0])
            win_rate = float(row.find("td", {
                             "class": "champion-stats__table__cell--winrate"}).text.strip().split("%")[0])
            boots.append((boots_id, pick_rate, win_rate))

        # add boots to frequent and highest win rate build
        frequent_core.append(
            sorted(boots, key=lambda e: e[1], reverse=True)[0][0])
        highest_core.append(
            sorted(boots, key=lambda e: e[2], reverse=True)[0][0])

        starters = []
        starters_rows = tables[2].find_all("tr")[1:]
        for row in starters_rows:
            items = []
            items_td = row.find(
                "td", {"class": "champion-stats__table__cell--data"})
            for item in items_td.find_all("li", {"class": "champion-stats__list__item"}):
                items.append(item.find("img").get("src").split("item")[1][1:5])
            pick_rate = float(row.find("td", {
                              "class": "champion-stats__table__cell--pickrate"}).text.strip().split("%")[0])
            win_rate = float(row.find("td", {
                             "class": "champion-stats__table__cell--winrate"}).text.strip().split("%")[0])
            starters.append((items, pick_rate, win_rate))

        frequent_starters = sorted(
            starters, key=lambda e: e[1], reverse=True)[0][0]
        highest_starters = sorted(
            starters, key=lambda e: e[2], reverse=True)[0][0]

        items = {
            "frequent": {
                "full": frequent_core,
                "starters": frequent_starters,
            },
            "highest": {
                "full": highest_core,
                "starters": highest_starters,
            }
        }

        return items

    def get_skill_order(self, champion, role):
        html = requests.get(
            f"https://euw.op.gg/champion/{champion['name']}/statistics/{role.lower()}/skill").text
        soup = BeautifulSoup(html, "html.parser")

        rows = soup.find(
            "table", {"class": "champion-stats__table--skill"}).find("tbody").children

        skill_orders = []

        for row in rows:

            try:
                skill_table = row.find(
                    "td", {"class": "champion-stats__table__cell--data"}).find("table")
                skills_row = skill_table.find_all("tr")[1]

                skills = []

                for skill_td in skills_row:

                    # need try/except because page loads pictures in some places
                    try:
                        skill = skill_td.text.strip()
                        skills.append(skill)
                    except:
                        pass

                pick_rate = float(row.find("td", {
                    "class": "champion-stats__table__cell--pickrate"}).text.strip().split("%")[0])
                win_rate = float(row.find("td", {
                    "class": "champion-stats__table__cell--winrate"}).text.strip().split("%")[0])

                skill_orders.append((skills, pick_rate, win_rate))

            except:
                pass

        skill_order = {
            "frequent": sorted(skill_orders, key=lambda e: e[1], reverse=True)[0][0],
            "highest": sorted(skill_orders, key=lambda e: e[2], reverse=True)[0][0]
        }

        return skill_order

    def get_version(self):
        html = requests.get("https://euw.op.gg/champion/statistics").text
        soup = BeautifulSoup(html, "html.parser")
        version = soup.find(
            "div", {"class": "champion-index__version"}).text.strip().split(" ")[-1]
        return version
