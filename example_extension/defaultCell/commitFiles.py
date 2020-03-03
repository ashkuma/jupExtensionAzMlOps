import os
import sys
import subprocess
import json
from sys import getsizeof

from IPython import get_ipython
from IPython.core.magics.namespace import NamespaceMagics

from jupextdemo.gitHubManager import GithubManager

DeploymentObject = {
    "githubPatToken": "GITHUBPATTOKEN"
}

gm = GithubManager(DeploymentObject["githubPatToken"])

repo = gm.getRepo()
gm.pushFiles(repo)
