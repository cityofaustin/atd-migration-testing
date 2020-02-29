"""
Prepare the new github issues for upload:
- add link to source issue
- add "migrated" label
- add new content to "github_payload element"
"""
import json
from os import listdir, remove
from os.path import isfile, join
import pdb

import requests

from config.config import DIR_GITHUB_CREATE, DIR_GITHUB_UPDATE, DEST_REPO
from config.secrets import GITHUB_USER, GITHUB_PASSWORD

from _logger import get_logger

def delete_issue(issue, directory):
    fname = f"{directory}/{issue['repo_name']}${issue['number']}.json"
    remove(fname)
    return True


def write_issue(issue, dest):
    fname = f"{dest}/{issue['repo_name']}${issue['number']}.json"

    with open(fname, "w") as fout:
        fout.write(json.dumps(issue))

    return True


def update_issue(issue):
    payload = {"body" : issue["body"]}
    url = issue["url"]
    res = requests.patch(url, json=payload, auth=(GITHUB_USER, GITHUB_PASSWORD))
    res.raise_for_status()
    return res


def update_body(issue):
    new_issue_number = issue["github_response"]["number"]
    new_url = f"https://github.com/cityofaustin/{DEST_REPO}/issues/{new_issue_number}"
    note = f"\n\n*Migrated to [{DEST_REPO} #{new_issue_number}]({new_url})*"
    return issue["body"] + note


def create_issue(issue, repo):
    logger.info(f"{issue['repo_name']} {issue['number']}")

    payload = issue["github_payload"]
    payload["assignees"] = [] # todo: REMOVE THIS!
    url = f"https://api.github.com/repos/cityofaustin/{repo}/issues"
    res = requests.post(url, json=payload, auth=(GITHUB_USER, GITHUB_PASSWORD))

    res.raise_for_status()

    logger.info(f"{repo} {res.json()['number']}")
    return res.json()

        

def load_issues(source_dir):
    issues = []

    fnames = [join(source_dir, f) for f in listdir(source_dir) if isfile(join(source_dir, f)) and f.endswith(".json")]

    for fname in fnames:
        with open(fname, "r") as fin:
            issue = json.loads(fin.read()) 
            issues.append(issue)

    return issues


def main():
    issues = load_issues(DIR_GITHUB_CREATE)

    for issue in issues:
        issue["github_response"] = create_issue(issue, DEST_REPO)
        issue["body"] = update_body(issue)
        write_issue(issue, DIR_GITHUB_UPDATE)
        delete_issue(issue, DIR_GITHUB_CREATE)
        res = update_issue(issue)
    
if __name__ == "__main__":
    logger = get_logger("github_create")
    main()