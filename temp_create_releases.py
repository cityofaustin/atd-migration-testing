"""
Set issue dependencies

https://github.com/ZenHubIO/API#create-a-dependency

{
  "blocking": {
    "repo_id": 92563409,
    "issue_number": 14
  },
  "blocked": {
    "repo_id": 92563409,
    "issue_number": 13
  }
}

"""

import json
import pdb
import time
import requests


import _utils
from config.config import DIR, DEST_REPO_ID
from config.secrets import ZENHUB_ACCESS_TOKEN
from _logger import get_logger

DEPEND_FILE = "dependencies_with_new_issue_numbers.json"



def zenhub_request(repo_id, payload):
    # limit requests to 100/min
    time.sleep(.6)
    
    url = f"https://api.zenhub.io/p1/repositories/{repo_id}/reports/release"

    params = {"access_token": ZENHUB_ACCESS_TOKEN}

    try:
        # handle exceptions for timeouts, connection, etc.
        pdb.set_trace()
        res = requests.post(url, params=params, json=payload)
        pdb.set_trace()
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
        data = json.loads(fin.read())

    for rel_id in data.keys():
        rel = data[rel_id]
        if rel.get("state") == "closed":
            continue
        rel.pop("issues")
        rel.pop("state")
        rel["repositories"] = [DEST_REPO_ID]
        rel.pop("release_id")
        rel.pop("created_at")
        rel.pop("closed_at")
        res = zenhub_request(DEST_REPO_ID, rel)
        pdb.set_trace()

if __name__ == "__main__":
    logger = get_logger("delete")
    main()
