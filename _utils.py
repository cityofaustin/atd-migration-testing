import json
from os import listdir, remove
from os.path import isfile, join

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