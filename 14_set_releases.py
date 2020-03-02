"""
Add issues to releases.
"""
import json
import pdb
import time
import requests

from config.config import DEST_REPO_ID
from config.secrets import ZENHUB_ACCESS_TOKEN
from _logger import get_logger

DEPEND_FILE = "dependencies_with_new_issue_numbers.json"


def zenhub_request(release_id, payload):
    # limit requests to 100/min
    time.sleep(.6)

    url = f"https://api.zenhub.io/p1/reports/release/{release_id}/issues"

    params = {"access_token": ZENHUB_ACCESS_TOKEN}

    try:
        # handle exceptions for timeouts, connection, etc.
        res = requests.patch(url, params=params, json=payload)
        console.log(res.status_code)
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
        if res.status_code == 500:
            return None

        if res.status_code == 404:
            print(res.text)
            return None

        if res.status_code == 403:
            print(res.text)
            return None

        else:
            print(e)
            return None

    return res.json()


def main():

    with open("releases_with_new_issue_numbers.json", "r") as fin:
        rels = json.loads(fin.read())

    # # TODO: FOR TESTING ONLY
    # with open("_temp_del_releases.json", "r") as fin:
    #     rel_map = {}
    #     rels_temp = json.loads(fin.read())
    #     for relid in rels_temp.keys():
    #         name = rels_temp[relid]["title"]
    #         rel_map[name] = relid

    for rel_id in rels:
        if rels[rel_id]["state"] == "closed":
            continue

        # title = rels[rel_id]["title"] # this mapping is only needed in test
        # try:
        #     mapped_id = rel_map[title]
        # except:
        #     pdb.set_trace() # emoji are killing this // will not be an issue in prod
        #     print("emoji fail")
        payload = {"add_issues": [], "remove_issues": []}

        if rels[rel_id]["issues"]:
            payload["add_issues"] = rels[rel_id]["issues"]
            res = zenhub_request(DEST_REPO_ID, payload)

            if not res:
                logger.error(f"ERROR: {payload}")

            else:
                logger.info(payload)


if __name__ == "__main__":
    logger = get_logger("set_releases")
    main()
