"""
Make sure all labels are created in the destination repo.

We do this by:
1. Downloading all labels in the destination repo
2. Downloading all labels in the source repo (which gives us name/color/description)
3. Loading new product labels from the label tracking worksheet
4. Extracting all labels from the source issues, which have already been mapped to new product labels
5. Identifying labels from the source issues are missing from the destination
6. Creating missing labels in the destination repo

"""
import csv
import json
from os import listdir
from os.path import isfile, join
import pdb

import requests

from config.config import DEST_REPO, DIR, LABEL_FILE, SOURCE_REPOS

from config.secrets import GITHUB_USER, GITHUB_PASSWORD
from _logger import get_logger


def get_missing_labels(dest_labels, label_defs, issue_labels):
    return [
        label_defs[label]
        for label in label_defs.keys()
        if label not in dest_labels and label in issue_labels
    ]


def get_labels_from_csv(fname):
    with open(fname, "r") as fin:
        reader = csv.DictReader(fin)
        return {
            label["name"]: {
                "name": label["name"],
                "color": label["color"],
                "description": label["description"],
            }
            for label in reader
            if label["action"] != "map"
        }


def get_labels_from_issues(source_directory):
    # get all labels from all issues
    fnames = [
        join(source_directory, f)
        for f in listdir(source_directory)
        if isfile(join(source_directory, f)) and f.endswith(".json")
    ]

    labels = []

    for fname in fnames:
        with open(fname, "r") as fin:
            issue = json.loads(fin.read())
            if issue["migration"].get("labels"):
                labels.extend(issue["labels"])

    return list(set(labels))


def get_labels_from_source_repos(repos):
    source_labels = {}

    for repo in repos:
        labels = get_labels_from_repo(repo["name"])

        for label in labels:
            if label["name"] not in source_labels:
                source_labels[label["name"]] = label

    return source_labels


def get_labels_from_repo(repo_name):
    labels = []

    url = f"https://api.github.com/repos/cityofaustin/{repo_name}/labels"

    last_url = None

    while True:
        res = requests.get(
            url, params={"per_page": 100}, auth=(GITHUB_USER, GITHUB_PASSWORD)
        )

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
        "name": label["name"],
        "color": label["color"],
        "description": label["description"],
    }

    res = requests.post(url, json=payload, auth=(GITHUB_USER, GITHUB_PASSWORD))

    res.raise_for_status()

    logger.info(f"{payload['name']}")

    return None


def main():
    # get all labels from destination repo (as list)
    dest_labels = get_labels_from_repo(DEST_REPO)

    dest_labels = [label["name"] for label in dest_labels]

    # get all labels from source repos
    source_labels = get_labels_from_source_repos(SOURCE_REPOS)

    # get all labels from label file
    file_labels = get_labels_from_csv(LABEL_FILE)

    # merge label definitions from file and source repos
    source_labels.update(file_labels)

    # get all labels from labeled issues
    issue_labels = get_labels_from_issues(DIR)

    create_labels = get_missing_labels(dest_labels, source_labels, issue_labels)

    for label in create_labels:
        logger.info(f"{label['name']}")
        create_label(label, DEST_REPO)


if __name__ == "__main__":
    logger = get_logger("create_labels")
    main()
