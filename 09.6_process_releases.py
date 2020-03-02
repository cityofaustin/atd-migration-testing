"""
Traverse all issues to fetch new issued ids for releases.
"""

from copy import deepcopy
import json
import pdb
import time
import requests

import _utils
from config.config import DIR, DEST_REPO_ID
from _logger import get_logger

SOURCE_FILE = "releases.json"
DEST_FILE = "releases_with_new_issue_numbers.json"


def drop_null_issues(releases):
    # drop any issues that do not have an issue number
    # these issues are closed/not being migrated
    new = {}

    for r_id in releases.keys():
        new[r_id] = deepcopy(releases[r_id])
        new[r_id]["issues"] = []

        for issue in releases[r_id]["issues"]:
            issue_number = issue["issue_number"]
            if issue_number:
                new[r_id]["issues"].append(issue)
    return new


def update_releases(releases, lookup):
    for r_id in releases.keys():
        for issue in releases[r_id]["issues"]:
            repo_id = issue["repo_id"]
            issue_number = issue["issue_number"]
            key = f"{repo_id}${issue_number}"
            issue["issue_number"] = lookup[key].get("new_issue_number")
            issue["repo_id"] = DEST_REPO_ID

    return releases


def build_lookup(releases):
    lookup = {}
    for r_id in releases.keys():
        for issue in releases[r_id]["issues"]:
            repo_id = issue["repo_id"]
            issue_number = issue["issue_number"]

            key = f"{repo_id}${issue_number}"
            lookup[key] = {"repo_id": repo_id, "issue_number": None}
    return lookup


def load_releases(fname):
    with open(fname, "r") as fin:
        data = json.loads(fin.read())

    return data


def main():
    # load all dependencies
    releases = load_releases(SOURCE_FILE)

    # make a dict of all issues that are in releases
    lookup = build_lookup(releases)

    # load all the issues
    issues = _utils.load_issues(DIR)

    # get the new issue number of every issue in a release
    for issue in issues:
        repo_id = issue.get("repo_id")
        issue_number = issue.get("number")
        key = f"{repo_id}${issue_number}"

        if key in lookup:
            new_issue_number = issue["migration"].get("new_issue_number")

            if not new_issue_number:
                # issue has apparently not been created in github
                logger.error(key)
                raise Exception(f"New {issue_number} does not exist in github!")

            lookup[key]["new_issue_number"] = new_issue_number

    # build new releases file
    releases = update_releases(releases, lookup)

    releases = drop_null_issues(releases)

    with open(DEST_FILE, "w") as fout:
        fout.write(json.dumps(releases))


if __name__ == "__main__":
    logger = get_logger("process_releases")
    main()
