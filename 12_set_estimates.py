"""
Set issue estimates
"""
import json
import pdb
import time
import requests


import _utils
from config.config import DIR, DEST_REPO_ID
from config.secrets import ZENHUB_ACCESS_TOKEN
from _logger import get_logger


def write_issue(issue, dest):
    fname = issue["path"]

    with open(fname, "w") as fout:
        fout.write(json.dumps(issue))

    return True


def zenhub_request(repo_id, issue_number, payload):
    # limit requests to 100/min
    time.sleep(.6)
    
    url = f"https://api.zenhub.io/p1/repositories/{repo_id}/issues/{issue_number}/estimate"
    
    params = {"access_token": ZENHUB_ACCESS_TOKEN}

    try:
        # handle exceptions for timeouts, connection, etc.
        res = requests.put(url, params=params, json=payload)

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

    issues = _utils.load_issues(DIR)

    for issue in issues:
        est = issue.get("estimate")

        if est:
            issue_number = issue.get("migration").get("new_issue_number")
            if issue_number:
                payload = {"estimate" : est["value"]}

                res = zenhub_request(DEST_REPO_ID, issue_number, payload)

                if not res:
                    logger.error(f"ERROR: {issue['path']}")
                    issue["migration"]["estimate_set"] = False
                else:
                    logger.info(issue["path"])
                    issue["migration"]["estimate_set"] = True

                write_issue(issue, DIR)

    
if __name__ == "__main__":
    logger = get_logger("set_estimates")
    main()