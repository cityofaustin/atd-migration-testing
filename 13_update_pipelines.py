"""
Set each issue pipeline in the right position.
"""
import json
import pdb
import time
import requests

import _utils
from config.config import DIR, DEST_REPO_ID, WORKSPACE_ID, SOURCE_REPOS
from config.secrets import ZENHUB_ACCESS_TOKEN
from _logger import get_logger


def write_issue(issue, dest):
    fname = issue["path"]

    with open(fname, "w") as fout:
        fout.write(json.dumps(issue))

    return True


def zenhub_request(repo_id, workspace_id, issue_number, payload):
    # limit requests to 100/min
    time.sleep(.6)

    url = f"https://api.zenhub.io/p2/workspaces/{workspace_id}/repositories/{repo_id}/issues/{issue_number}/moves"

    params = {"access_token": ZENHUB_ACCESS_TOKEN}

    try:
        # handle exceptions for timeouts, connection, etc.
        res = requests.post(url, params=params, json=payload)

    except requests.exceptions.Timeout:
        print("timeout")
        return None

    except:
        print("unknwon error")
        return None

    try:
        # handle status code errors
        res.raise_for_status()

    except Exception as e:
        # handle an edge case where an issue is not found in zenub
        if res.status_code == 500:
            return None

        if res.status_code == 404:
            print(res.text)
            return None

        if res.status_code == 403:
            print(res.text)
            return None

        else:
            print(e)
            return None

    return True


def get_test_pipelines():
    # import requests
    # from config.secrets import ZENHUB_ACCESS_TOKEN
    # REPO_ID = 244223631
    # params = {"access_token": ZENHUB_ACCESS_TOKEN}
    # # 5e5c2b60f434330225542b02 test board
    # url = "https://api.zenhub.io/p2/workspaces/5e5c2b60f434330225542b02/repositories/244223631/board"
    # res = requests.get(url, params=params)
    # bob = res.json()
    # stu = [{"id" : pipe["id"], "name" : pipe["name"]} for pipe in bob["pipelines"]]
    # return None
    return [
        {"id": "5e5c2b60f43433474f542afc", "name": "New Issues"},
        {"id": "5e5c2b60f434332f28542afd", "name": "Icebox"},
        {"id": "5e5c3f0c71016ea705f1e2c2", "name": "Needs Scoping"},
        {"id": "5e5c2b60f43433db7a542afe", "name": "Backlog"},
        {"id": "5e5c3f1d71016ecee7f1e2c7", "name": "On Deck"},
        {"id": "5e5c3f3771016eb178f1e2ce", "name": "Blocked"},
        {"id": "5e5c2b60f434331a05542aff", "name": "In Progress"},
        {"id": "5e5c3f3b71016ed31cf1e2d1", "name": "Recurring"},
        {"id": "5e5c2b60f434333d31542b00", "name": "Review/QA"},
        {"id": "5e5c3f5271016e3c77f1e2da", "name": "Ready to Deploy"},
    ]


def sort_issues(issues):
    # sort all issues by their position
    unsorted_issues = []

    for issue in issues:
        issue_number = issue.get("migration").get("new_issue_number")
        position = issue.get("migration").get("pipeline").get("position")
        unsorted_issues.append({"position": position, "data": issue})

    return sorted(unsorted_issues, key=lambda k: k["position"])


def replace_pipe(pipe_map, pipe_name):
    for pipe in pipe_map:
        if pipe.get("name") == pipe_name:
            return pipe.get("id")
    return None


def main():

    # test only
    test_pipes = get_test_pipelines()

    # assign positions to issues
    issues = _utils.load_issues(DIR)
    sorted_issues = sort_issues(issues)

    for issue_element in sorted_issues:
        issue = issue_element.get("data")
        issue_number = issue.get("migration").get("new_issue_number")
        pos = issue.get("migration").get("pipeline").get("position")

        # TODO: TEST ONLY. Prod just use existing pipeline ID
        # pipe_id = issue.get("migration").get("pipeline").get("pipeline_id")
        pipe_name = issue.get("migration").get("pipeline").get("pipeline_name")
        pipe_id = replace_pipe(test_pipes, pipe_name)

        payload = {"pipeline_id": pipe_id, "position": pos}

        res = zenhub_request(DEST_REPO_ID, WORKSPACE_ID, issue_number, payload)

        if not res:
            logger.error(f"ERROR: {issue['path']}")
            issue["migration"]["pipeline_processed"] = False
        else:
            logger.info(issue["path"])
            issue["migration"]["pipeline_processed"] = True

        write_issue(issue, DIR)


if __name__ == "__main__":
    logger = get_logger("update_pipelines")
    main()
