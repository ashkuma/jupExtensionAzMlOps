import requests
import json
import time
try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse
from jupextdemo.const import (CHECKIN_MESSAGE_AKS, APP_NAME_DEFAULT, APP_NAME_PLACEHOLDER,
                              ACR_PLACEHOLDER, RG_PLACEHOLDER, PORT_NUMBER_DEFAULT,
                              CLUSTER_PLACEHOLDER, RELEASE_PLACEHOLDER, RELEASE_NAME)

_git_remotes = {}
_GIT_EXE = 'git'

_HTTP_NOT_FOUND_STATUS = 404
_HTTP_SUCCESS_STATUS = 200
_HTTP_CREATED_STATUS = 201


class Files:  # pylint: disable=too-few-public-methods
    def __init__(self, path, content):
        self.path = path
        self.content = content


def getLocalRepoUrl():
    localUrls = get_git_remotes()
    x = None
    if localUrls != None:
        print(localUrls)
        x = localUrls["origin(fetch)"]

    return x if is_github_url_candidate(x) else None


def compareUrls(uri1, uri2):
    if (uri1 == None and uri2 != None) or (uri1 != None and uri2 == None) or (uri1 == None and uri2 == None):
        return False

    components1 = uri_parse(uri1.lower())
    components2 = uri_parse(uri2.lower())

    if (components1.netloc == "github.com" and components1.netloc == components2.netloc) and components2.path == components1.path:
        return True
    else:
        return False


def uri_parse(url):
    return urlparse(url)


def is_github_url_candidate(url):
    if url is None:
        return False
    components = uri_parse(url.lower())
    if components.netloc == 'github.com':
        return True
    return False


def get_git_remotes():
    import subprocess
    import sys
    if _git_remotes:
        return _git_remotes
    try:
        # Example output:
        # git remote - v
        # full  https://mseng.visualstudio.com/DefaultCollection/VSOnline/_git/_full/VSO (fetch)
        # full  https://mseng.visualstudio.com/DefaultCollection/VSOnline/_git/_full/VSO (push)
        # origin  https://mseng.visualstudio.com/defaultcollection/VSOnline/_git/VSO (fetch)
        # origin  https://mseng.visualstudio.com/defaultcollection/VSOnline/_git/VSO (push)
        output = subprocess.check_output(
            [_GIT_EXE, 'remote', '-v'], stderr=subprocess.STDOUT)
    except BaseException as ex:  # pylint: disable=broad-except
        print("Not a repo")
        return None
    if sys.stdout.encoding is not None:
        lines = output.decode(sys.stdout.encoding).split('\n')
    else:
        lines = output.decode().split('\n')
    for line in lines:
        components = line.strip().split()
        if len(components) == 3:
            _git_remotes[components[0] + components[2]] = components[1]
    return _git_remotes


def get_application_json_header():
    return {'Content-Type': 'application/json' + '; charset=utf-8',
            'Accept': 'application/json'}

def get_application_json_header_for_preview():
    return {'Accept': 'application/vnd.github.antiope-preview+json'}

def get_check_runs_for_commit(repo_name,repo_owner, commmit_sha,token):
    """
    API Documentation - https://developer.github.com/v3/checks/runs/#list-check-runs-for-a-specific-ref
    """
    headers = get_application_json_header_for_preview()

    get_check_runs_url = 'https://api.github.com/repos/{owner}/{repo_id}/commits/{ref}/check-runs'.format(owner=repo_owner,
        repo_id=repo_name, ref=commmit_sha)
    print(get_check_runs_url)
    get_response = requests.get(url=get_check_runs_url, auth=('', token), headers=headers)
    if not get_response.status_code == 200:
        print(" could not find the valid url")
        print(get_response)
        return
    import json
    return json.loads(get_response.text)


def get_work_flow_check_runID(repo_name, repo_owner, commmit_sha,token):
    check_run_found = False
    count = 0
    while(not check_run_found or count > 3):
        check_runs_list_response = get_check_runs_for_commit(repo_name,repo_owner, commmit_sha, token)
        if check_runs_list_response and check_runs_list_response['total_count'] > 0:
            # fetch the Github actions check run and its check run ID
            check_runs_list = check_runs_list_response['check_runs']
            for check_run in check_runs_list:
                if check_run['app']['slug'] == 'github-actions':
                    check_run_id = check_run['id']
                    check_run_found = True
                    return check_run_id
        time.sleep(5)
        count = count + 1
    return None


def get_check_run_status_and_conclusion(repo_name, repo_owner, check_run_id, token):
    """
    API Documentation - https://developer.github.com/v3/checks/runs/#get-a-single-check-run
    """
    headers = get_application_json_header_for_preview()
    get_check_run_url = 'https://api.github.com/repos/{owner}/{repo_id}/check-runs/{checkID}'.format(owner=repo_owner,
        repo_id=repo_name, checkID=check_run_id)
    get_response = requests.get(url=get_check_run_url, auth=('', token), headers=headers)
    if not get_response.status_code == _HTTP_SUCCESS_STATUS:
        print(" no valid status code")
        return
    import json
    return json.loads(get_response.text)['status'], json.loads(get_response.text)['conclusion']


def poll_workflow_status(repo_name, repo_owner, check_run_id, token):
    import colorama
    import humanfriendly
    import time
    check_run_status = None
    check_run_status, check_run_conclusion = get_check_run_status_and_conclusion(repo_name,repo_owner, check_run_id, token)

    if check_run_status == 'completed':
        print("already completed")
    elif check_run_status == 'queued':
        # When workflow status is Queued
        colorama.init()
        with humanfriendly.Spinner(label="Workflow is in queue") as spinner:
            while True:
                spinner.step()
                time.sleep(0.5)
                check_run_status, check_run_conclusion = get_check_run_status_and_conclusion(repo_name,repo_owner, check_run_id, token)
                if check_run_status in ('in_progress', 'completed'):
                    break
        colorama.deinit()
    elif check_run_status == 'in_progress':
        # When workflow status is inprogress
        colorama.init()
        with humanfriendly.Spinner(label="Workflow is in progress") as spinner:
            while True:
                spinner.step()
                time.sleep(0.5)
                check_run_status, check_run_conclusion = get_check_run_status_and_conclusion(repo_name,repo_owner, check_run_id, token)
                if check_run_status == 'completed':
                    break
        colorama.deinit()
    print('GitHub workflow completed.')
    return (check_run_status, check_run_conclusion)
