import json
from pprint import pprint as print
import pdb
import time

from github import Github
import requests

from config.config import SOURCE_REPOS, DIR_GITHUB
from config.secrets import GITHUB_USER, GITHUB_PASSWORD
from _logger import get_logger
"""
TODO:
Do we have all the repos??
product label colors!
Update this sheet for the label mapping:
https://docs.google.com/spreadsheets/d/1pTum5oFfDpIo575zAYDPA_bdsEfoElpCO1-HzAU68wk/edit#gid=651251559

filter out epics, pipelines not in our main workspace

- fix labels in atd-data-tech. not all project labels are in the dts service bot settings!
- apply product labels < move to separate script
- depenencies
- milestone validation, etc.


FLOW:
- add missing labels
- and that all labels are mapped to products
- only open issues!? no. migrate closed. - what about epics with closed issues???
- get all issues and zenhub data
- write to JSON
- create all issues in github (milestones, labels, assignees, title, body, state)
- each time issue is created:
    - close/link to new issues/apply "migrated" label
    - write to JSON
- convert issues to epics
- add issues to epics
- move issuses to pipeline
- set a special migrated label!


## fields
- title
- body
- assignee
- estimate
- epic
- old url
- new url
- milestone
- pipeline
- release
- attachements?
"""




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
