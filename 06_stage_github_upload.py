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

import _utils
from config.config import DIR

from _logger import get_logger


def write_issues(issues, dest):
    issue_count = 0

    for issue in issues:
        fname = f"{dest}/{issue['repo_name']}${issue['number']}.json"

        with open(fname, "w") as fout:
            logger.info(f"{issue['repo_name']} {issue['number']}")
            fout.write(json.dumps(issue))
            issue_count += 1
    return issue_count


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


def main():
    issues = _utils.load_issues(DIR)

    for issue in issues:
        issue["migration"]["github_payload"] = build_payload(issue)
        issue["migration"]["github_payload"]["body"] = update_body(issue)
        issue["migration"]["github_payload"]["labels"].append("migrated")

    issue_count = write_issues(issues, DIR)
    logger.info(f"Issues Processed: {issue_count}")

if __name__ == "__main__":
    logger = get_logger("stage_github_upload")
    main()
