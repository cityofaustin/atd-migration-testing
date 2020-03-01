"""
Download Zenhub metadata for all issues.
"""
import json
from os import listdir
from os.path import isfile, join, split
from pprint import pprint as print
import pdb
from shutil import copyfile
import time

import requests

import _utils
from config.config import DIR
from config.secrets import ZENHUB_ACCESS_TOKEN
from _logger import get_logger


def zenhub_request(url, issue_no):
    url = f"{url}{issue_no}"
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
            print(f"not found: {issue_no}")
            return None

        if res.status_code == 403:
            print(res.text)
            return None

        else:
            print(e)
            return none

    return res.json()


def get_zenhub_issue(issue):

    zenhub_endpoint = (
        f"https://api.zenhub.io/p1/repositories/{issue['repo_id']}/issues/"
    )

    zenhub_issue = zenhub_request(zenhub_endpoint, issue["number"])

    if not zenhub_issue:
        # some zenhub issues are mysteriously not found
        print("NO ZENHUB")
        return None

    else:
        issue["pipelines"] = zenhub_issue.get("pipelines")
        issue["estimate"] = zenhub_issue.get("estimate")
        issue["is_epic"] = zenhub_issue.get("is_epic")

    issue["migration"]["zenhub_downloaded"] = True
    return issue


def get_epic_issues(issue):
    zenhub_endpoint = f"https://api.zenhub.io/p1/repositories/{issue['repo_id']}/epics/"

    epic = zenhub_request(zenhub_endpoint, issue["number"])
    issue["epic_issues"] = epic["issues"]
    return issue


def main():

    issues = _utils.load_issues(DIR)

    for issue in issues:

        time.sleep(.6)  # zenhub rate limit is 100 requests/minute

        try:
            issue = get_zenhub_issue(issue)
        except:
            issue["migration"]["zenhub_downloaded"] = False
            logger.error(f)
            continue

        if issue["is_epic"]:
            get_epic_issues(issue)

        fname = issue["path"]

        with open(fname, "w") as fout:
            logger.info(f"{issue['repo_name']} {issue['number']}")
            fout.write(json.dumps(issue))


if __name__ == "__main__":
    logger = get_logger("download_zenhub")
    main()
