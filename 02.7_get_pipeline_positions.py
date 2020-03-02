"""
Get/write the pipeline position into issue > migration > pipeline
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


def zenhub_request_get(repo_id, workspace_id):
    # limit requests to 100/min
    time.sleep(.6)
    
    url = f"https://api.zenhub.io/p2/workspaces/{workspace_id}/repositories/{repo_id}/board"
    
    params = {"access_token": ZENHUB_ACCESS_TOKEN}

    try:
        # handle exceptions for timeouts, connection, etc.
        res = requests.get(url, params=params)

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

    return res.json()


def get_board_issues():
    # import requests
    # from config.secrets import ZENHUB_ACCESS_TOKEN
    # REPO_ID = 244223631
    # url = f"https://api.zenhub.io/p2/repositories/244223631/workspaces"
    # params = {"access_token": ZENHUB_ACCESS_TOKEN}
    # # 5e5c2b60f434330225542b02 test board
    # url = "https://api.zenhub.io/p2/workspaces/5e5c2b60f434330225542b02/repositories/244223631/board"
    # res = requests.get(url, params=params)
    # stu = [{"id" : pipe["id"], "name" : pipe["name"]} for pipe in bob["pipelines"]]
    return None

def get_pipelines():
    # test board
    return [{'id': '5e5c2b60f43433474f542afc', 'name': 'New Issues'}, {'id': '5e5c2b60f434332f28542afd', 'name': 'Icebox'}, {'id': '5e5c3f0c71016ea705f1e2c2', 'name': 'Needs Scoping'}, {'id': '5e5c2b60f43433db7a542afe', 'name': 'Backlog'}, {'id': '5e5c3f1d71016ecee7f1e2c7', 'name': 'On Deck'}, {'id': '5e5c3f3771016eb178f1e2ce', 'name': 'Blocked'}, {'id': '5e5c2b60f434331a05542aff', 'name': 'In Progress'}, {'id': '5e5c3f3b71016ed31cf1e2d1', 'name': 'Recurring'}, {'id': '5e5c2b60f434333d31542b00', 'name': 'Review/QA'}, {'id': '5e5c3f5271016e3c77f1e2da', 'name': 'Ready to Deploy'}]

def main():
    test_pipes = get_pipelines()

    issues_with_positions = {}

    for repo in SOURCE_REPOS:
        # fetch all the issues in the workspace to get issue positions

        if repo["id"] == 140626918:
            """
            we skip in atd-data-tech
            Those issue will not have pipelines updated,
            but do need to reconnect the dependencies, etc.
            """
            print("yep")
            continue

        pipelines = zenhub_request_get(repo["id"], WORKSPACE_ID)

        for pipe in pipelines.get("pipelines"):
            for issue in pipe.get("issues"):
                
                key = f"{repo['id']}${issue['issue_number']}"
                
                issues_with_positions[key] = {
                    "old_issue_number" : issue['issue_number'],
                    "pipeline_id" : pipe.get("id"),
                    "pipeline_name" : pipe.get("name"),
                    "position" : issue.get("position"),
                    "repo_id" : DEST_REPO_ID
                }

    # assign positions to issues
    issues = _utils.load_issues(DIR)

    for issue in issues:
        repo_id = issue.get("repo_id")
        
        if repo["id"] == 140626918:
            """
            we skip in atd-data-tech
            Those issue will not have pipelines updated,
            but do need to reconnect the dependencies, etc.
            """
            continue

        issue_number = issue.get("number")
        key = f"{repo_id}${issue_number}"
        issue["migration"]["pipeline"] = issues_with_positions.get(key)
        write_issue(issue, DIR)

    
if __name__ == "__main__":
    logger = get_logger("apply_pipeline_positions")
    main()