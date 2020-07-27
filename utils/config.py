import json
import os


def get(key):
    """ Get value from key in config """
    home_path = os.path.expanduser("~")

    # if config is made
    if os.path.isfile(os.path.join(home_path, ".lolbuilds", "config.json")):
        with open(os.path.join(home_path, ".lolbuilds", "config.json")) as f:
            config = json.load(f)

        if key in config:
            return config[key]

    # config is not made or config does not contain key
    return None


def save(key, value):
    """ Save a (key, value) pair to the local config file in ~/.lolbuilds/config.json """
    home_path = os.path.expanduser("~")

    try:
        os.makedirs(os.path.join(home_path, ".lolbuilds"))

    except FileExistsError:
        # config already exists, open the config dict and add new value
        with open(os.path.join(home_path, ".lolbuilds", "config.json"), "r") as f:
            config = json.load(f)
            config[key] = value

        # save config dict with new value
        with open(os.path.join(home_path, ".lolbuilds", "config.json"), "w") as f:
            f.write(json.dumps(config))

    else:
        # config is created for the first time
        with open(os.path.join(home_path, ".lolbuilds", "config.json"), "w") as f:
            config = {}
            config[key] = value
            f.write(json.dumps(config))
