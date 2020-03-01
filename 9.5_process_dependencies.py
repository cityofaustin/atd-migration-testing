"""
https://github.com/ZenHubIO/API#create-a-dependency

go through each dependency go through each issue,
update the depencies with the new issue number and new repo id

write missing dependencies to a file.

write a new dependencies file which can serve as a zenhub dependency payload.
"""


import json
import pdb
import time
import requests

import _utils
from config.config import DIR, DEST_REPO_ID
from _logger import get_logger

SOURCE_FILE = "dependencies.json"
DEST_FILE = "dependencies_with_new_issue_numbers.json"
MISSING_DEPEND_FILE = "missing_dependency_issues.json"


def build_new_dependencies(depends, lookup):

    for d in depends:
        for key in d.keys():
            issue_number = d[key]["issue_number"]
            repo_id = d[key]["repo_id"]
            lookup_key = f"{repo_id}${issue_number}"
            d[key]["issue_number"] = lookup[lookup_key]["new_issue_number"]
            # we hardcode the destination repo id to the migration destination repo
            d[key]["repo_id"] = DEST_REPO_ID

    return depends
    

def build_d_lookup(depends):
    lookup = {}
    for d in depends:
        for key in d.keys():
            issue_number = d[key]["issue_number"]
            repo_id = d[key]["repo_id"]
            key = f"{repo_id}${issue_number}"
            lookup[key] = {}
            lookup[key]["new_issue_number"] = None
    
    return lookup


def load_dependencies(fname):
    with open(fname, "r") as fin:
        data = json.loads(fin.read())

    return data


def main():
    missing_dependency_issues = []

    # load all dependencies
    depends = load_dependencies(SOURCE_FILE)

    # make a dict of all issues that are blocking or blocked
    d_lookup = build_d_lookup(depends)

    # load all the issues
    issues = _utils.load_issues(DIR)

    for issue in issues:
        repo_id = issue.get("repo_id")
        issue_number = issue.get("number")
        key = f"{repo_id}${issue_number}"
        
        if key in d_lookup:
            new_issue_number = issue["migration"].get("new_issue_number")
            
            if not new_issue_number:
                # issue has apparently not been created in github
                logger.error(key)
                raise Exception(f"New {issue_number} does not exist in github!")
            
            d_lookup[key]["new_issue_number"] = new_issue_number

        else:
            # issue must be closed, because we haven't downloaded it
            missing_dependency_issues.append(key)

    # build new dependencies file
    depends = build_new_dependencies(depends, d_lookup)

    with open(DEST_FILE, "w") as fout:
        fout.write(json.dumps(depends))


    with open(MISSING_DEPEND_FILE, "w") as fout:
        fout.write(json.dumps(missing_dependency_issues))

        
if __name__ == "__main__":
    logger = get_logger("process_dependencies")
    main()

