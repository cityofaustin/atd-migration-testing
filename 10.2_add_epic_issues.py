"""
Convert issues to epics and add issues to those epics.

https://github.com/ZenHubIO/API#convert-an-epic-to-an-issue

build a list of all epics
    - with an array of the new issues + repo ids that are part of the epic
    - convert issues to epics with child issues
    - mark as processed
"""

# POST /p1/repositories/:repo_id/issues/:issue_number/convert_to_epic

# {
#   "issues": [
#     { "repo_id": 13550592, "issue_number": 3 },
#     { "repo_id": 13550592, "issue_number": 1 }
#   ]
# }

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


def zenhub_request(repo_id, issue_number, issues):
    # limit requests to 100/min
    time.sleep(.6)

    url = f"https://api.zenhub.io/p1/repositories/{repo_id}/issues/{issue_number}/update_issues"

    params = {"access_token": ZENHUB_ACCESS_TOKEN}

    try:
        # handle exceptions for timeouts, connection, etc.
        res = requests.post(url, params=params, json=issues)

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

    return True  # no data is returned from a 200 status when creating epics


def main():

    issues = _utils.load_issues(DIR)

    for issue in issues:

        if issue.get("is_epic"):

            # new issue number of issue that will be converted to epic
            issue_number = issue["migration"].get("new_issue_number")

            payload = {"add_issues": []}

            for e in issue["epic_issues"]:
                if e.get("repo_id") == 140626918 and issue.get("repo_id") == 140626918:
                    """
                    We do not need to add issues to epics that are already
                    in atd-data-tech when the issue is already in atd-data-tech.
                    Are you confused yet? This is a complication of the fact that
                    an epic might contain a mix of issues that are being migrated
                    and which already exist in the destination repo :/
                    """
                    continue

                if e.get("new_issue_number"):
                    payload["issues"].append(
                        {"repo_id": DEST_REPO_ID, "issue_number": e["new_issue_number"]}
                    )

            if payload["add_issues"]:
                res = zenhub_request(DEST_REPO_ID, issue_number, payload)

                if not res:
                    logger.error(f"ERROR: {issue['path']}")
                    issue["migration"]["epic_created"] = False
                else:
                    logger.info(issue["path"])

                issue["migration"]["epic_created"] = True

                write_issue(issue, DIR)


if __name__ == "__main__":
    logger = get_logger("convert_epics")
    main()
