"""
Make sure all of the milestones exist in the destination repo.
"""
import json
from os import listdir
from os.path import isfile, join
import pdb

import requests

import _utils
from config.config import DIR, DEST_REPO
from config.secrets import GITHUB_USER, GITHUB_PASSWORD

from _logger import get_logger


def write_issues(issues, dest):
    issue_count = 0
    for issue in issues:
        fname = issue["path"]

        with open(fname, "w") as fout:
            logger.info(f"{issue['repo_name']} {issue['number']}")
            fout.write(json.dumps(issue))
            issue_count += 1
    return issue_count


def update_milestones(issues, milestones):
    # map the milestone to the milestone number in the dest repo
    # if the dest repo does not have the milestone, the milestone is dropped
    update_count = 0

    for issue in issues:
        m = issue.get("milestone")
        if m:
            if m in milestones:
                issue["migration"]["milestone"] = milestones[m]["number"]
                logger.info(f"{m}")
                update_count += 1
            else:
                issue["migration"]["milestone"] = None
                logger.error(f"Milestone not found: {m}")
        else:
            issue["migration"]["milestone"] = None

    return issues, update_count


def get_milestones_from_repo(repo_name):
    milestones = {}

    url = f"https://api.github.com/repos/cityofaustin/{repo_name}/milestones"

    last_url = None

    while True:
        res = requests.get(
            url, params={"per_page": 100}, auth=(GITHUB_USER, GITHUB_PASSWORD)
        )

        res.raise_for_status()

        for m in res.json():
            milestones[m["title"]] = {"title": m["title"], "number": m["number"]}

        if url == last_url:
            break

        try:
            links = requests.utils.parse_header_links(res.headers["Link"])
        except KeyError:
            # if there's only one page there will be no link headers
            break

        if links:
            for link in links:
                if link.get("rel") == "next":
                    url = link.get("url")
                    print(url)
                elif link.get("rel") == "last":
                    last_url = link.get("url")

    return milestones


def main():
    issues = _utils.load_issues(DIR)
    
    dest_milestones = get_milestones_from_repo(DEST_REPO)

    issues, update_count = update_milestones(issues, dest_milestones)

    issue_count = write_issues(issues, DIR)
    logger.info(f"Issues Processed: {issue_count}")
    logger.info(f"Milestones Updated: {update_count}")

if __name__ == "__main__":
    logger = get_logger("set_milestones")
    main()
