import os
import sys
import subprocess
import json
from sys import getsizeof

from IPython import get_ipython
from IPython.core.magics.namespace import NamespaceMagics

from jupextdemo.gitHubManager import GithubManager

DeploymentObject = {
    "acrDetails" : "ACRPLACEHOLDER",
    "aksDetails" : "AKSPLACEHOLDER",
    "githubPatToken" : "GITHUBPATTOKEN"
}

print(DeploymentObject)


print(GithubManager(DeploymentObject["githubPatToken"]).getRepo())


