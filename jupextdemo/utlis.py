import os
import sys
import subprocess
import json
from os.path import dirname, abspath

ACR_PLACEHOLDER = 'container_registry_name_place_holder'
APP_NAME_PLACEHOLDER = 'app_name_place_holder'
PORT_NUMBER_PLACEHOLDER = 'port_number_place_holder'
CLUSTER_PLACEHOLDER = 'cluster_name_place_holder'
RG_PLACEHOLDER = 'resource_name_place_holder'

PORT_NUMBER_DEFAULT = '8080'
APP_NAME_DEFAULT = 'k8sdemo'
RELEASE_NAME = 'aksappupdemo'

# Checkin message strings

CHECKIN_MESSAGE_AKS = 'Setting up AKS deployment workflow'
CHECKIN_MESSAGE_FUNCTIONAPP = 'Setting up Functionapp deployment workflow'

RELEASE_PLACEHOLDER = 'release_name_place_holder'

BASE_DIR = abspath(dirname(dirname(abspath(__file__))))
PACKS_ROOT_STRING = os.path.sep + 'resources' + os.path.sep + 'packs' + os.path.sep
FILE_ABSOLUTE_PATH = abspath(dirname(dirname(abspath(__file__))))




def getHelmCharts(acr_details,port):
    languagePackPath = getLanguagePackPath()
    print(languagePackPath)
    print(" ")
    files = []
    langfilesPaths = testglob(languagePackPath)
    #print(langfilesPaths)
    for name in langfilesPaths :
        if "charts" not in name:
            continue
        if "values.yaml" in name :
            file_content = get_file_content(name)
            print(name)
        if name.startswith(languagePackPath):
            name = name[len(languagePackPath):]
        else:
            print(name + " doesn start with" + langfilesPaths)
        files.append(name)
    return files




def getLanguagePackPath():
    
    return BASE_DIR + os.path.sep + PACKS_ROOT_STRING + "python" + os.path.sep


def testglob(langpath):
    import glob
    return glob.glob(langpath+"**", recursive=True);
    


def replace_values(file_content, acr_details):
    content = file_content.replace(APP_NAME_PLACEHOLDER, APP_NAME_DEFAULT).replace(ACR_PLACEHOLDER, acr_details['name'])
    return content


def replace_port(file_content, port):
    content = file_content.replace(PORT_NUMBER_PLACEHOLDER, port)
    return content


def get_file_content(path):
    try:
        filecontent = open(path).read()
        return filecontent
    except Exception as ex:
        print(ex)



def getUserSubscriptionsList():
    accountsList = json.loads(subprocess.check_output("az account list -o json", shell=True))
    s={}
    for acc in accountsList :
        s[acc['id']]=acc["name"]
    
    print(s)





