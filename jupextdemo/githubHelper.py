import requests
import json

try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse

_git_remotes = {}
_GIT_EXE = 'git'


def isValidRepoForPat():
    # get url from local repo
    
    print(" now using the PAT to verify this local directory is in the same account as for which PAT is generated")
    gm = GithubManager("<PAT TOKEN>")
    for repo in gm. g.get_user().get_repos():
        if compareUrls(x,repo.clone_url):
            print(" both urls are same ");
        else:
            print("PAT is not valid for this repository")

def getLocalRepoUrl():
    localUrls = get_git_remotes();
    x=None
    if localUrls != None:
        print(localUrls)
        x = localUrls["origin(fetch)"]
        
    return x if is_github_url_candidate(x) else None;

        
def compareUrls(uri1 , uri2):
    if (uri1 == None and uri2 != None) or (uri1 != None and uri2 == None) or  (uri1 == None and uri2 == None):
        return False
    
    components1 = uri_parse(uri1.lower())
    components2 = uri_parse(uri2.lower())

    if (components1.netloc == "github.com" and components1.netloc == components2.netloc) and components2.path == components1.path:
        return True;
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
        output = subprocess.check_output([_GIT_EXE, 'remote', '-v'], stderr=subprocess.STDOUT)
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


    