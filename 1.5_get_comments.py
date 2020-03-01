"""
- Create new github issues
- Update source issue with a link to the new issue
"""
from datetime import datetime
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


def parse_comments(comments):
    # extract comment and prepend user name
    parsed = []
    
    for comment in comments:
        body = comment["body"]
        user = comment["user"]["login"]
        stamp = comment["updated_at"][0:10] # lazily just grabbing the date from the timestamp
        body = f"*From {user} on {stamp}*:\n\n{body}"
        parsed.append({"uploaded" : False, "body" : body})

    return parsed


def get_comments(repo, issue_number):
    url = f"https://api.github.com/repos/cityofaustin/{repo}/issues/{issue_number}/comments"

    res = requests.get(url, auth=(GITHUB_USER, GITHUB_PASSWORD))

    res.raise_for_status()

    return res.json()


def main():
    issues = _utils.load_issues(DIR)

    for issue in issues:
        issue["comments"] = get_comments(issue["repo_name"], issue["number"])
        issue["comments"] = parse_comments(issue["comments"])
        issue["migration"]["comments_retreived"] = True
        write_issue(issue, DEST_REPO)

if __name__ == "__main__":
    logger = get_logger("download_comments")
    main()
