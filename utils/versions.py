import requests
import json


def get_lol_version():
    """ Get current League of Legends version """
    versions = json.loads(requests.get(
        "https://ddragon.leagueoflegends.com/api/versions.json").text)
    # reformats from 10.14.5 to 10.14
    latest = ".".join(versions[0].split(".")[:2])
    return latest
