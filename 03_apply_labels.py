"""
Add/replace labels on issues. These changes are written back to the issue JSON
and included in the github payload when the new issue is create.
"""
import csv
import json
from os import listdir
from os.path import isfile, join

import pdb
from pprint import pprint as print

import _utils
from config.config import DIR, LABEL_FILE, REPO_MAP
from config.secrets import GITHUB_USER, GITHUB_PASSWORD

from _logger import get_logger


def write_issue(issue, directory):
    fname = issue["path"]

    with open(fname, "w") as fout:
        logger.info(f"{issue['repo_name']} {issue['number']}")
        fout.write(json.dumps(issue))

    return True


def map_repos(labels, repo_name, repo_map):
    label = repo_map.get(repo_name)

    if label and label not in labels:
        labels.append(label)

    return labels


def map_labels(labels, label_lookup):
    new_labels = []
    # TODO handle map_append vs map
    for label in labels:
        if label in label_lookup:
            dest_label_action = label_lookup[label]
            dest_label, action = dest_label_action.split("_&_")
            if action == "map":
                # replace label with lookup label
                logger.info(f"{label} >> {dest_label}")
                new_labels.append(dest_label)
            elif action =="map_append":
                logger.info(f"{label} >> {dest_label}")
                new_labels.append(label)
                new_labels.append(dest_label)
        else:
            new_labels.append(label)

    return new_labels


def get_issue(fname):
    with open(fname, "r") as fin:
        return json.loads(fin.read())


def build_lookup(label_map):
    lookup = {}
    for row in label_map:
        label_src = row["name"]
        label_dest = row["corresponding product label"]
        label_action = row["action"]
        # disgusting hack because i'm tired of writing this  migation
        # we have to be able to distinguish between map and map/append
        # label actions. i don't want to refactor all the code so 
        # we're squeezing the action into the destination label_name
        label_dest = label_dest + "_&_" + label_action
        lookup[label_src] = label_dest

    return lookup


def main():
    with open(LABEL_FILE, "r") as fin:
        reader = csv.DictReader(fin)
        label_map = [row for row in reader if "map" in row["action"]]

        label_lookup = build_lookup(label_map)

    issues = _utils.load_issues(DIR)

    for issue in issues:
        labels = issue.get("labels")
        labels = map_labels(labels, label_lookup)
        labels = map_repos(labels, issue["repo_name"], REPO_MAP)
        issue["migration"]["labels"] = labels
        write_issue(issue, DIR)


if __name__ == "__main__":
    logger = get_logger("apply_labels")
    main()
