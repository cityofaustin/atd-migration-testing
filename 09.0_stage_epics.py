"""
Traverse issues and update epics with the new issue IDs of their child issues.

If the child issue is not found, write it to missing_epic_issues.json.


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

import requests

import _utils
from config.config import DIR, DEST_REPO, DEST_REPO_ID

from _logger import get_logger

MISSING_CHILDREN_FILE = "missing_epic_issues.json"


def write_issue(issue, dest):
    fname = issue["path"]

    with open(fname, "w") as fout:
        fout.write(json.dumps(issue))

    return True


def main():
    missing_epic_issues = []
    child_issues = {}

    issues = _utils.load_issues(DIR)

    issue_count = 0
    epic_count = 0
    child_issue_count = 0

    # iterate through all issues, identify epics, and collect their child issues
    for issue in issues:
        if not issue.get("is_epic"):
            continue

        for child_issue in issue["epic_issues"]:
            repo_id = child_issue["repo_id"]
            issue_number = child_issue["issue_number"]
            key = f"{repo_id}${issue_number}"
            child_issues[key] = {"repo_id": repo_id, "issue_number": issue_number}

    # iterate through all issues and identify new issue numbers of child issues
    for issue in issues:
        key = f"{issue['repo_id']}${issue['number']}"
        if key in child_issues:
            issue_number = issue["migration"].get("new_issue_number")

            if not issue_number:
                raise Exception(f"{key} does not have a new github issue number!")

            child_issues[key]["new_issue_number"] = issue_number

    # update epics' child issues with their new issue numbers
    for issue in issues:
        issue_count += 1

        if not issue.get("is_epic"):
            continue


        for child_issue in issue["epic_issues"]:
            repo_id = child_issue["repo_id"]
            issue_number = child_issue["issue_number"]
            key = f"{repo_id}${issue_number}"
            new_issue_number = child_issues[key].get("new_issue_number")
            child_issue["new_issue_number"] = new_issue_number
            child_issue_count += 1

            if not new_issue_number:
                # child issue has not been processed, it's probably a closed issue
                # which we're not migrating
                missing_epic_issues.append(
                    {
                        "repo_id": child_issue["repo_id"],
                        "issue_number": child_issue["issue_number"],
                    }
                )

        # write update issue to file
        issue["migration"]["epics_staged"] = True
        write_issue(issue, DIR)
        epic_count += 1

    logger.info(f"Issues Processed: {issue_count}")
    logger.info(f"Epics Processed: {epic_count}")
    logger.info(f"Child Issues Processed: {child_issue_count}")

    with open(MISSING_CHILDREN_FILE, "w") as fout:
        fout.write(json.dumps(missing_epic_issues))
# logger.info(f"Issues Processed: {issue_count}")

if __name__ == "__main__":
    logger = get_logger("stage_epics")
    main()
