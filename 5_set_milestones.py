"""
Make sure all of the milestones exist in the destination repo.
"""
import json
from os import listdir
from os.path import isfile, join
import pdb

import requests

from config.config import DIR_LABELED, DEST_REPO, DIR_MILESTONES

from config.secrets import GITHUB_USER, GITHUB_PASSWORD

from _logger import get_logger


def write_issues(issues, dest):
    for issue in issues:
        fname = f"{dest}/{issue['repo_name']}${issue['number']}.json"

        with open(fname, "w") as fout:
            logger.info(f"{issue['repo_name']} {issue['number']}")
            fout.write(json.dumps(issue))
    return True


def update_milestones(issues, milestones):
    # map the milestone to the milestone number in the dest repo
    # if the dest repo does not have the milestone, the milestone is dropped
    for issue in issues:
        m = issue.get("milestone")
        if m:
            if m in milestones:
                issue["milestone"] = milestones[m]["number"]
                logger.info(f"{m}")
            else:
                issue.pop("milestone")
                logger.error(f"pop: {m}")

    return issues



def get_milestones_from_repo(repo_name):
    milestones = {}

    url = f"https://api.github.com/repos/cityofaustin/{repo_name}/milestones"

    last_url = None
    
    while True:
        res = requests.get(url, params={"per_page":100}, auth=(GITHUB_USER, GITHUB_PASSWORD))
        
        res.raise_for_status()

        for m in res.json():
            milestones[m["title"]] = {"title" : m["title"], "number" : m["number"]}

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


def load_issues(source_dir):
    issues = []

    fnames = [join(source_dir, f) for f in listdir(source_dir) if isfile(join(source_dir, f)) and f.endswith(".json")]

    for fname in fnames:
        with open(fname, "r") as fin:
            issue = json.loads(fin.read()) 
            issues.append(issue)

    return issues


def main():
    issues = load_issues(DIR_LABELED)
    dest_milestones = get_milestones_from_repo(DEST_REPO)

    issues = update_milestones(issues, dest_milestones)

    write_issues(issues, DIR_MILESTONES)
    
if __name__ == "__main__":
    logger = get_logger("set_milestones")
    main()
