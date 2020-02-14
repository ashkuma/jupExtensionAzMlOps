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
PACKS_ROOT_STRING = os.path.sep + 'resources' + \
    os.path.sep + 'packs' + os.path.sep
FILE_ABSOLUTE_PATH = abspath(dirname(dirname(abspath(__file__))))


class Files:  # pylint: disable=too-few-public-methods
    def __init__(self, path, content):
        self.path = path
        self.content = content


def getHelmCharts(acr_details, port):
    languagePackPath = getLanguagePackPath()
    files = []
    langfilesPaths = testglob(languagePackPath)
    for name in langfilesPaths:
        if not os.path.isfile(name):
            continue
        if "charts" not in name:
            continue
        file_content = get_file_content(name)
        if "values.yaml" in name:
            file_content = replace_values(file_content, acr_details)
            file_content = replace_port(file_content, port)
        if name.startswith(languagePackPath):
            name = name[len(languagePackPath):]
            name = name.replace('\\', '/')

            files.append(Files(path=name, content=file_content))
    return files


def get_yaml_template_for_repo(cluster_details, acr_details, repo_name):
    files_to_return = []
    github_workflow_path = '.github/workflows/'
    # Read template file
    yaml_file_name = 'main.yml'
    workflow_yaml = github_workflow_path + yaml_file_name
    from resources.resourcefiles import DEPLOY_TO_AKS_TEMPLATE
    files_to_return.append(Files(path=workflow_yaml,
                                 content=DEPLOY_TO_AKS_TEMPLATE
                                 .replace(APP_NAME_PLACEHOLDER, APP_NAME_DEFAULT)
                                 .replace(ACR_PLACEHOLDER, acr_details['name'])
                                 .replace(CLUSTER_PLACEHOLDER, cluster_details['name'])
                                 .replace(RELEASE_PLACEHOLDER, RELEASE_NAME)
                                 .replace(RG_PLACEHOLDER, cluster_details['resourceGroup'])))
    return files_to_return


def get_docker_templates(language, port):
    files = []
    language_packs_path = getLanguagePackPath()
    docker_file_path = r'Dockerfile'
    file_path = FILE_ABSOLUTE_PATH + language_packs_path + docker_file_path
    file_content = get_file_content(file_path)
    docker_file_content = replace_port(file_content, port)
    docker_file = Files(path=docker_file_path, content=docker_file_content)
    print("Checkin file path: %s" % (docker_file.path))
    print("Checkin file content: %s" % (docker_file.content))
    files.append(docker_file)
    docker_ignore_path = r'.dockerignore'
    file_path = FILE_ABSOLUTE_PATH + language_packs_path + docker_ignore_path
    docker_ignore_content = get_file_content(file_path)
    docker_ignore = Files(path=docker_ignore_path,
                          content=docker_ignore_content)
    print("Checkin file path: %s" % (docker_ignore.path))
    print("Checkin file content: %s" % (docker_ignore.content))
    files.append(docker_ignore)
    return files


def getLanguagePackPath():
    return BASE_DIR + os.path.sep + PACKS_ROOT_STRING + "python" + os.path.sep


def testglob(langpath):
    import glob
    return glob.glob(langpath+"**", recursive=True)


def replace_values(file_content, acr_details):
    print(acr_details)
    acr_name = acr_details['name'] if (
        acr_details != None and "name" in acr_details) else APP_NAME_DEFAULT
    content = file_content.replace(
        APP_NAME_PLACEHOLDER, APP_NAME_DEFAULT).replace(ACR_PLACEHOLDER, acr_name)
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
    accountsList = json.loads(subprocess.check_output(
        "az account list -o json", shell=True))
    s = {}
    for acc in accountsList:
        s[acc['id']] = acc["name"]

    print(s)
    return s


def getDefaultSubcriptionInfo():
    subscriptionList = getUserSubscriptionsList()
    for subscription in subscriptionList:
        if subscription['isDefault']:
            return subscription['id'], subscription['name'], subscription['tenantId'], subscription['environmentName']
    print(
        'Your account does not have a default Azure subscription. Please run \'az login\' to setup account.')
    return None, None, None, None


def configure_aks_credentials(cluster_name, resource_group):
    try:
        subscription_id, subscription_name, tenant_id, environment_name = getDefaultSubcriptionInfo()
        print("Using your default Azure subscription %s for getting AKS cluster credentials.",
              subscription_name)
        _aks_creds = subprocess.check_output(
            'az aks get-credentials -n {cluster_name} -g {group_name} -o json'.format(
                cluster_name=cluster_name, group_name=resource_group), shell=True)
        # print(_aks_creds)
    except Exception as ex:
        print(ex)


def get_deployment_IP_port(release_name, language):
    if not which('kubectl'):
        print('Can not find kubectl executable in PATH')
    try:
        import subprocess
        import json
        service_name = release_name + '-' + language.lower()
        service_details = subprocess.check_output(
            'kubectl get service {} -o json'.format(service_name), shell=True)
        service_obj = json.loads(service_details)
        deployment_ip = service_obj['status']['loadBalancer']['ingress'][0]['ip']
        port = service_obj['spec']['ports'][0]['port']
        return deployment_ip, port
    except subprocess.CalledProcessError as err:
        print('Could not find app/service: {}'.format(err))


def which(binary):
    path_var = os.getenv('PATH')
    import platform
    if platform.system() == 'Windows':
        binary = binary + '.exe'
        parts = path_var.split(';')
    else:
        parts = path_var.split(':')

    for part in parts:
        bin_path = os.path.join(part, binary)
        if os.path.exists(bin_path) and os.path.isfile(bin_path) and os.access(bin_path, os.X_OK):
            return bin_path

    return None
