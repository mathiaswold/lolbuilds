import json
import os


def get(key):
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


def save(key, value):
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
