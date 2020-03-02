"""
Update new github issues w/ comments
"""
import json
from os import listdir, remove
from os.path import isfile, join
import pdb

import requests

import _utils
from config.config import DIR, DEST_REPO
from config.secrets import GITHUB_USER, GITHUB_PASSWORD

from _logger import get_logger


def write_issue(issue, dest):
    fname = issue["path"]

    with open(fname, "w") as fout:
        fout.write(json.dumps(issue))

    return True


def create_comment(issue_number, repo, body):

    url = f"https://api.github.com/repos/cityofaustin/{repo}/issues/{issue_number}/comments"

    res = requests.post(url, json={"body": body}, auth=(GITHUB_USER, GITHUB_PASSWORD))

    res.raise_for_status()

    logger.info(f"{issue_number} {repo} {body}")
    return res.json()


def main():
    issues = _utils.load_issues(DIR)

    for issue in issues:
        # skip issues which have not been created:
        issue_number = issue.get("migration").get("new_issue_number")

        if not issue_number:
            # this should never happen. all issue should exist by now
            logger.error(f"Error: {issue['path']}")
            continue
        
        if issue.get("repo_id") == 140626918:
            """
            We do not create comments for issues from atd-data-tech,
            Because that's the repo we're migrating to,
            But we do need to reference these isssue
            To connect the dependencies and epics to new issues.
            """
            continue

        # skip issues which already have comments created
        if issue.get("comments"):
            for comment in issue["comments"]:
                if not comment.get("uploaded"):
                    res = create_comment(issue_number, DEST_REPO, comment["body"])
                    comment["uploaded"] = True
                    write_issue(issue, DEST_REPO)

if __name__ == "__main__":
    logger = get_logger("github_create_comments")
    main()
