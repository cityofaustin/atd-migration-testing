"""
Prepare the new github issues for upload:
- add link to source issue
- add "migrated" label
- add new content to "github_payload element"
"""
import json
from os import listdir
from os.path import isfile, join
import pdb

from config.config import DIR

from _logger import get_logger


def write_issues(issues, dest):
    for issue in issues:
        fname = f"{dest}/{issue['repo_name']}${issue['number']}.json"

        with open(fname, "w") as fout:
            logger.info(f"{issue['repo_name']} {issue['number']}")
            fout.write(json.dumps(issue))
    return True


def update_body(issue):
    number = issue.get("number")
    repo = issue.get("repo_name")
    source_url = f"https://github.com/cityofaustin/{repo}/issues/{number}"
    body = issue.get("body")
    note = f"\n\n*Migrated from [{repo} #{number}]({source_url})*"
    body = body + note
    return body


def build_payload(issue):
    GITHUB_FIELDS = ["assignees", "state", "title", "body"]
    payload = {key: issue[key] for key in issue.keys() if key in GITHUB_FIELDS}
    payload["labels"] = issue["migration"].get("labels")
    payload["milestone"] = issue["migration"].get("milestone")
    return payload


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


def main():
    issues = load_issues(DIR)

    for issue in issues:
        issue["migration"]["github_payload"] = build_payload(issue)
        issue["migration"]["github_payload"]["body"] = update_body(issue)
        issue["migration"]["github_payload"]["labels"].append("migrated")

    write_issues(issues, DIR)


if __name__ == "__main__":
    logger = get_logger("stage_github_upload")
    main()
