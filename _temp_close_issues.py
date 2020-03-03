"""
Download all issues from Github.
"""
import json
from pprint import pprint as print
import pdb
import time

from github import Github
import requests

from config.config import SOURCE_REPOS, DIR
from config.secrets import GITHUB_USER, GITHUB_PASSWORD
from _logger import get_logger


def get_repo(g, repo, org="cityofaustin"):
    return g.get_repo(f"{org}/{repo}")


def main():

    g = Github(GITHUB_USER, GITHUB_PASSWORD)


    repo = get_repo(g, "atd-monorepo-testing")

    open_issues = repo.get_issues(state='open')
    count =0
    for issue in open_issues:
        count +=1 
        print(count)
        issue.edit(state='closed')

if __name__ == "__main__":
    logger = get_logger("download_github")
    main()
