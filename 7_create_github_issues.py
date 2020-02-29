"""
- Create new github issues
- Update source issue with a link to the new issue
"""
import json
from os import listdir, remove
from os.path import isfile, join
import pdb

import requests

from config.config import DIR, DEST_REPO
from config.secrets import GITHUB_USER, GITHUB_PASSWORD

from _logger import get_logger


def write_issue(issue, dest):
    fname = issue["path"]

    with open(fname, "w") as fout:
        fout.write(json.dumps(issue))

    return True


def update_issue(issue):
    payload = {
        "body": issue["migration"]["source_body_update"],
        "labels": issue["labels"],
    }

    # append special "migrated" label
    payload["labels"].append("migrated")

    url = issue["url"]
    res = requests.patch(url, json=payload, auth=(GITHUB_USER, GITHUB_PASSWORD))
    res.raise_for_status()
    return res.json()


def update_body(body, number, repo):
    url = f"https://github.com/cityofaustin/{repo}/issues/{number}"
    note = f"\n\n*Migrated to [{repo} #{number}]({url})*"
    return body + note


def create_issue(issue, repo):
    logger.info(f"{issue['repo_name']} {issue['number']}")

    payload = issue["migration"]["github_payload"]
    payload["assignees"] = []  # todo: REMOVE THIS!
    url = f"https://api.github.com/repos/cityofaustin/{repo}/issues"
    res = requests.post(url, json=payload, auth=(GITHUB_USER, GITHUB_PASSWORD))

    res.raise_for_status()

    logger.info(f"{repo} {res.json()['number']}")
    return res.json()


def load_issues(source_dir):
    issues = []

    fnames = [
        join(source_dir, f)
        for f in listdir(source_dir)
        if isfile(join(source_dir, f)) and f.endswith(".json")
    ]

    for fname in fnames:
        with open(fname, "r") as fin:
            issue = json.loads(fin.read())
            issues.append(issue)

    return issues


def main():
    issues = load_issues(DIR)

    for issue in issues:
        # skip issues which have already been created
        if issue.get("migration").get("created_github"):
            continue

        res = create_issue(issue, DEST_REPO)
        issue["migration"]["created_github"] = True
        issue["migration"]["new_issue_number"] = res["number"]
        write_issue(issue, DIR)
        issue["migration"]["source_body_update"] = update_body(
            issue["body"], res["number"], DEST_REPO
        )
        res = update_issue(issue)
        issue["migration"]["updated_source_github"] = True
        write_issue(issue, DIR)


if __name__ == "__main__":
    logger = get_logger("github_create")
    main()
