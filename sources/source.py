from utils import config, files


class Source:

    def __init__(self, name, get_champions, get_items, get_skill_order, get_version):
        self.name = name
        self.get_champions = get_champions
        self.get_items = get_items
        self.get_skill_order = get_skill_order
        self.get_version = get_version

    def get_item_sets(self, champion):
        """ Gets item sets with items and skill order for every role for a champion """

        item_sets = []

        for role, role_rank in champion["roles"]:

            items = self.get_items(champion, role)
            skill_order = self.get_skill_order(champion, role)

            item_set = {
                "role": role,
                "rank": role_rank,
                "frequent": {
                    "full": items["frequent"]["full"],
                    "starters": items["frequent"]["starters"],
                    "skill_order": skill_order["frequent"]
                },
                "highest": {
                    "full": items["highest"]["full"],
                    "starters": items["highest"]["starters"],
                    "skill_order": skill_order["highest"]
                }
            }

            item_sets.append(item_set)

        return item_sets

    def import_item_sets(self):
        champions = self.get_champions()
        version = self.get_version()

        config.save(self.name, version)

        for champion in champions:
            print(
                f"Adding {champion['display_name']}'s item sets from {self.name}...", end="\r")

            item_sets = self.get_item_sets(champion)

            for item_set in item_sets:
                files.save(champion, item_set, version, self.name)

            print(" "*80, end="\r")
