import json
from sys import getsizeof

from IPython import get_ipython
from IPython.core.magics.namespace import NamespaceMagics

from jupextdemo.azaks_deploy import *

_nms = NamespaceMagics()
_Jupyter = get_ipython()
_nms.shell = _Jupyter.kernel.shell

try:
    import numpy as np  # noqa: F401
except ImportError:
    pass


import os

import subprocess

replyObject = {};

aks_dep = AKSDeploy();
if aks_dep.IsUserLoggedIn() :
    replyObject["DefaultSubscription"] = aks_dep.getDefaultSubscription()
else:
    aks_dep.loginUserFlow()
    replyObject["DefaultSubscription"] = aks_dep.getDefaultSubscription() 

# get ACR details
replyObject["ACRAccount"] = aks_dep.getACRDetails()

# get AKS details
replyObject["AKSCluster"] =  aks_dep.getAKSDetails()

print(json.dumps(replyObject));