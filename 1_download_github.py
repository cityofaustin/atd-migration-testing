"""
Download all issues from Github.
"""
import json
from pprint import pprint as print
import pdb
import time

from github import Github
import requests

from config.config import SOURCE_REPOS, DIR_GITHUB
from config.secrets import GITHUB_USER, GITHUB_PASSWORD
from _logger import get_logger

def get_repo(g, repo, org="cityofaustin"):
    return g.get_repo(f"{org}/{repo}")


def main():

    g = Github(GITHUB_USER, GITHUB_PASSWORD)

    for r in SOURCE_REPOS:
        repo = get_repo(g, r["name"])
        issues = repo.get_issues()
        
        for issue in issues:
            if issue.pull_request:
                print("PR")
                continue

            new_issue = {
                "repo_name" : r["name"],
                "repo_id" : r["id"],
                "assignees" : [person.login for person in issue.assignees],
                "labels" : [label.name for label in issue.labels],
                "state" : issue.state,
                "url" : issue.url,
                "number" : issue.number,
                "title" : issue.title,
                "body" : issue.body,
            }

            if issue.milestone:
                new_issue["milestone"] = issue.milestone.title

            fname = f"{DIR_GITHUB}/{new_issue['repo_name']}${new_issue['number']}.json"
            
            with open(fname, "w") as fout:
                logger.info(f"{new_issue['repo_name']} {new_issue['number']}")
                fout.write(json.dumps(new_issue))

if __name__ == "__main__":
    logger = get_logger("download_github")
    main()
