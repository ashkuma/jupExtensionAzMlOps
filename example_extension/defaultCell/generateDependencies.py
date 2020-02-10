import json
from sys import getsizeof

from IPython import get_ipython
from IPython.core.magics.namespace import NamespaceMagics

_nms = NamespaceMagics()
_Jupyter = get_ipython()
_nms.shell = _Jupyter.kernel.shell

try:
    import numpy as np  # noqa: F401
except ImportError:
    pass


# this will take a config object and generate two things 1) dockerfile  2) wrapper file. 
# command to refresh the list of variables
# requireMentObject = {}
# dockerTemplateObject={'From' : "", 'FilesFoldersAdd':[], 'preinstallCommands':[], 'startCommand':"" }
# appFileObject ={'path':"",'pickelFilePath':""}


# def checkRequirementFile():
#     pass

# def checkAppFileExist():
#     pass

# def checkDockerFileExist():
#     pass

# creates a docker file
# f = open("Dockerfile","w+");
# f.write("FROM python:3 \nADD app.py / \nADD azdevopsdemo.pkl / \nADD PewDiePie.csv / \nADD requirements.txt / \n# Expose the port \nRUN pip install --upgrade pip \nRUN pip install -r /requirements.txt \nEXPOSE 80 \n# Set the working directory \nWORKDIR / \n# Run the flask server for the endpoints \nCMD python app.py");
# f.close()

# _groupObject = {'requireMentObject':requireMentObject,'dockerTemplateObject':dockerTemplateObject, 'appFileObject':appFileObject}
# print(json.dumps(_groupObject));