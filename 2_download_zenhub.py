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

from config.config import DIR_GITHUB, DIR_ZENHUB, FAILDIR
from config.secrets import ZENHUB_ACCESS_TOKEN
from _logger import get_logger


def handle_error(f):
    # move failed issues to special dir
    fname = split(f)[-1]
    dest = join(FAILDIR, fname)
    copyfile(f, dest)
    logger.error(f)
    return None


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

    return issue


def get_epic_issues(issue):
    zenhub_endpoint = (
        f"https://api.zenhub.io/p1/repositories/{issue['repo_id']}/epics/"
    )

    epic = zenhub_request(zenhub_endpoint, issue["number"])
    issue["epic_issues"] = epic["issues"]
    return issue


def main():

    issue_files = [join(DIR_GITHUB, f) for f in listdir(DIR_GITHUB) if isfile(join(DIR_GITHUB, f)) and f.endswith(".json")]

    for f in issue_files:
        with open(f, "r") as fin:

            issue = json.loads(fin.read())

            time.sleep(.6) # zenhub rate limit is 100 requests/minute
    
            issue = get_zenhub_issue(issue)
            
            if not issue:
                handle_error(f)
                continue

            if issue["is_epic"]:
                get_epic_issues(issue)

            fname = f"{DIR_ZENHUB}/{issue['repo_name']}${issue['number']}.json"
            
            with open(fname, "w") as fout:
                logger.info(f"{issue['repo_name']} {issue['number']}")
                fout.write(json.dumps(issue))

if __name__ == "__main__":
    logger = get_logger("download_zenhub")
    main()
