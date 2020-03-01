"""
Download all releases from zenhub and write to releases.json
"""
import json
import pdb
import time
import requests


from config.config import SOURCE_REPOS
from config.secrets import ZENHUB_ACCESS_TOKEN
from _logger import get_logger

outfile = "releases.json"


def convert_to_dict(releases):
    new = {}

    for r in releases:
        release_id = r.get("release_id")
        new[release_id] = r

    return new

def zenhub_request(url):

    params = {"access_token": ZENHUB_ACCESS_TOKEN}

    try:
        # handle exceptions for timeouts, connection, etc.
        res = requests.get(url, params=params)

    except requests.exceptions.Timeout:
        print("timeout")
        return None

    except:
        print("unknwon error")
        return None

    try:
        # handle status code errors
        res.raise_for_status()

    except Exception as e:
        # handle an edge case where an issue is not found in zenub
        if res.status_code == 404:
            print(res.text)
            return None

        if res.status_code == 403:
            print(res.text)
            return None

        else:
            print(e)
            return none

    return res.json()


def main():
    
    releases = []

    # get all releases (there will be duplicates, because multiple repos can hold the same release)
    for repo in SOURCE_REPOS:
        repo_id = repo["id"]
        url = f"https://api.zenhub.io/p1/repositories/{repo_id}/reports/releases"
        res = zenhub_request(url)
        
        if res == None:
            logger.error(repo_id)

        releases.extend(res)

    releases = convert_to_dict(releases)

    # get all issues in a release
    for r_id in releases.keys():
        print(releases[r_id]["title"])
        url = f"https://api.zenhub.io/p1/reports/release/{r_id}/issues"    
        res = zenhub_request(url)

        if res == None:
            logger.error(r_id)

        releases[r_id]["issues"] = res

    with open(outfile, "w") as fout:
        fout.write(json.dumps(releases))

if __name__ == "__main__":
    logger = get_logger("get_releases")
    main()