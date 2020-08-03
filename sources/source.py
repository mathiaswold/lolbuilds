from utils import config, files


class Source:

    def __init__(self, name, roles=True):
        """
        Template for source classes. 
        The source should implement the methods described below, with the correct return values.

        Parameters:
        - name (str): Name of source. Gets used in file path. Should be all lowercase, letters only.
        - roles (bool): If source categorizes item sets (builds) by role
        """
        self.name = name
        self.roles = roles

    def get_champions(self):
        """
        - Returns a list of champions in dictonary format
            - Returned dictionary format: 
                {
                    "name": str, 
                    "display_name": str, 
                    "id": str, 
                    "roles": list [OPTIONAL]
                }
                - Roles doesn't need to be included if source does not categorize item sets by role
        """
        raise NotImplementedError

    def get_items(self, champion, role):
        """
        Parameters:
        - champion (dict): dict returned from get_champions
        - OPTIONAL: role (str): role to get items from, if self.roles == True

        Returns:
        - Dictionary with items for this champion and role
            - Returned dictionary format: 
                {
                    "frequent": {
                        "full": list, 
                        "starters": list
                    }, 
                    "highest": {
                        "full": list, 
                        "starters": list
                    }
                }
        """
        raise NotImplementedError

    def get_skill_order(self, champion, role):
        """
        Parameters:
        - champion (dict): dict returned from get_champions
        - OPTIONAL: role (str): role to get skill order from, if self.roles == True

        Returns:
        - Dictionary with skill order for this champion and role
            - Returned dictionary format: 
                {
                    skill_order = {
                        "frequent": list,
                        "highest": list
                    }
                }
            -List example (length 18): ["Q", "W", "E", ..., "R", "E", "E"]
        """
        raise NotImplementedError

    def get_version(self):
        """
        Returns:
        - Current version of the source in string format, e.g. "10.14" or "2020.10.20"
        """
        raise NotImplementedError

    def get_item_sets(self, champion):
        """ Gets item sets with items and skill order for every role (if supported) for a champion """

        item_sets = []

        # roles supported, create an item set per role
        if self.roles:
            for counter, role in enumerate(champion["roles"]):
                try:
                    items = self.get_items(champion, role)
                    skill_order = self.get_skill_order(champion, role)

                    item_set = {
                        "role": role,
                        # add sort_rank if roles are supported, higher sort rank equals higher position in the item set list in-game
                        "sort_rank": 10 - counter,
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
                except:
                    print(
                        f"ERROR: Build for {champion['display_name']} {role} not found on {self.name}")

        # roles not supported, create only one item set
        else:
            try:
                items = self.get_items(champion)
                skill_order = self.get_skill_order(champion)

                item_set = {
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

            except:
                print(
                    f"ERROR: Build for {champion['display_name']} not found on {self.name}")

        return item_sets

    def import_item_sets(self):
        """ Imports all item sets for all champions and roles """

        # first remove old item sets
        self.delete_item_sets()

        champions = self.get_champions()
        version = self.get_version()

        config.save(self.name, version)

        for champion in champions:
            print(
                f"Importing {champion['display_name']}'s item sets from {self.name}...")

            item_sets = self.get_item_sets(champion)

            for item_set in item_sets:
                files.save(champion, item_set, version, self.name, self.roles)

    def delete_item_sets(self):
        """ Deletes all item sets for all champions and roles generated by import_item_sets """

        print(f"Deleting item sets from {self.name}")

        config.save(self.name, None)

        try:
            champions = self.get_champions()
        except:
            print(
                f"ERROR: Could not delete item sets from {self.name}. This likely happened because of a bad connection to {self.name}.")
            return

        for champion in champions:
            files.delete(champion, self.name)
