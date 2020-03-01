"""
Download all dependecies from zenhub
"""
import json
import pdb
import time
import requests


from config.config import SOURCE_REPOS
from config.secrets import ZENHUB_ACCESS_TOKEN
from _logger import get_logger

outfile = "dependencies.json"

def zenhub_request(repo_id):
    url = f"https://api.zenhub.io/p1/repositories/{repo_id}/dependencies/"
    
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
        if res.status_code == 404:
            print(res.text)
            return None

        if res.status_code == 403:
            print(res.text)
            return None

        else:
            print(e)
            return none

    return res.json()


def main():

    all_dependencies = []

    for repo in SOURCE_REPOS:
        repo_id = repo["id"]
        res = zenhub_request(repo_id)
        
        if res == None:
            logger.error(repo_id)

        all_dependencies.extend(res["dependencies"])
    
    with open(outfile, "w") as fout:
        fout.write(json.dumps(all_dependencies))
        
if __name__ == "__main__":
    logger = get_logger("get_dependencies")
    main()