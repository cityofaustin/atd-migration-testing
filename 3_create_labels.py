
import csv
import json
import pdb

import requests

from config.config import DEST_REPO, LABEL_FILE, SOURCE_REPOS

from config.secrets import GITHUB_USER, GITHUB_PASSWORD
from _logger import get_logger

"""
make sure all labels are created in the destination repo

TODO: map labels before creating missing
TODO: change dest repo
"""

def get_labels(repo_name):
    labels = []

    url = f"https://api.github.com/repos/cityofaustin/{repo_name}/labels"

    last_url = None
    
    while True:
        res = requests.get(url, params={"per_page":100}, auth=(GITHUB_USER, GITHUB_PASSWORD))
        
        res.raise_for_status()

        for label in res.json():
            label["repo"] = repo_name
            labels.append(label)

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

    return labels


def reduce_labels(labels):
    reduced = []
    keys = []

    for label in labels:
        if label["name"] not in keys:
            keys.append(label["name"])
            reduced.append(label)
        else:
            continue

    return reduced


def create_label(label, repo_name):
    url = f"https://api.github.com/repos/cityofaustin/{repo_name}/labels"
    
    payload = {
        "name" : label["name"],
        "color" : label["color"],
        "description" : label["description"]
    }

    res = requests.post(url, json=payload, auth=(GITHUB_USER, GITHUB_PASSWORD))

    res.raise_for_status()
    
    return None


def main():

    # read in new labels we've defined in a csv, excluding those that will be mapped to another label
    with open(LABEL_FILE, "r") as fin:
        reader = csv.DictReader(fin)
        loaded_labels = [row for row in reader if row["action"] != "map"]

    labels = [{"name": label["name"], "color":label["color"], "description" : label["description"] } for label in loaded_labels]

    # get all labels from all repos
    for repo in SOURCE_REPOS:
        repo_labels = get_labels(repo["name"])
        labels.extend(repo_labels)

    labels = reduce_labels(labels)

    # get all labels from destination repo:
    dest_labels = get_labels(DEST_REPO)

    create_labels = []

    for label in labels:
        matched = False

        name = label["name"]
        
        for dest_label in dest_labels:
            if dest_label["name"] == name:
                matched = True
                break

        if not matched:
            create_labels.append(label)

    # TODO: map labels
    for label in create_labels:
        logger.info(f"{label['name']}")
        pdb.set_trace() 
        create_label(label, DEST_REPO)


if __name__ == "__main__":
    logger = get_logger("create_labels")
    main()
