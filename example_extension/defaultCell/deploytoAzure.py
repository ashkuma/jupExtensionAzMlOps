import os
import sys
import subprocess
import json
from sys import getsizeof

from IPython import get_ipython
from IPython.core.magics.namespace import NamespaceMagics

from jupextdemo.gitHubManager import GithubManager

DeploymentObject = {
    "acrName": "ACRPLACEHOLDER",
    "aksName": "AKSNAMEPLACEHOLDER",
    "aksResourceGroup": "AKSRESOURCEGROUPPLACEHOLDER",
    "githubPatToken": "GITHUBPATTOKEN"
}

gm = GithubManager(DeploymentObject["githubPatToken"])

gm.pushDeployFilestoRepo(
    {"name": DeploymentObject["aksName"], "resourceGroup": DeploymentObject["aksResourceGroup"]}, {"name": DeploymentObject["acrName"]})
