from github import Github, GithubException
from .utils import *
from .githubHelper import *
from .azaks_deploy import AKSDeploy
from jupextdemo.const import (
    AZURE_CREDENTIALS, REGISTRY_USERNAME, REGISTRY_PASSWORD)


class GithubManager():
    def __init__(self, patToken):
        self.patToken = patToken
        self.g = Github(self.patToken)
        self.repo = None
        self.aksDeploy = AKSDeploy()

    def _getNewToken(self):
        return self.patToken

    def pushDeployFilestoRepo(self, cluster_details, acr_details):
        # 1 assume language as python
        # 2 assume we are in the same repo, from where is it invoking
        # 3 assuming user already has docker file
        # assuming helmCharts and workflow have to be pushed
        repo = self.getRepo()
        self.pushGithubSecrets(repo)
        returnCommit = None
        if repo == None:
            print("PAT entered is not for the correct owner of this repository. Make sure you are in the repository and notebook is opened from that repo only. ")
            return
        ifChartsExists = self.chartsExist(repo)
        ifWorkFlowExists = self.workFlowFileExists(repo)
        if not ifChartsExists:
            self.pushCharts(repo, acr_details, PORT_NUMBER_DEFAULT)

        if not ifWorkFlowExists:
            returnCommit = self.pushWorkFlow(
                repo, cluster_details, acr_details)
            self.getWorkflowStatus(returnCommit['commit'].sha, cluster_details)

        if ifChartsExists and ifWorkFlowExists:
            commit = self.pushdummyFiles(self.repo)
            self.getWorkflowStatus(commit['commit'].sha, cluster_details)

    def pushGithubSecrets(self, repo):
        repoFullName = repo.owner.login + "/" + repo.name
        if not self.checkIfSecretExists(repoFullName, AZURE_CREDENTIALS):
            azCredentials = self.aksDeploy.getAzureCredentials()
            self.createRepoSecret(repo, AZURE_CREDENTIALS, azCredentials)
        if not self.checkIfSecretExists(repoFullName, REGISTRY_USERNAME):
            secretValue = self.aksDeploy.getServicePrinciple()
            self.createRepoSecret(repo, REGISTRY_USERNAME,
                                  secretValue["appId"])
            self.createRepoSecret(repo, REGISTRY_PASSWORD,
                                  secretValue["password"])

    def getRepo(self):
        # TODO : check if this works when i am in any branch as well
        x = getLocalRepoUrl()
        for repo in self. g.get_user().get_repos():
            if compareUrls(x, repo.clone_url):
                self.repo = repo
                return repo

        return None

    def pushTestFile(self):
        pass

    def pushCharts(self, repo, acr_details, port=PORT_NUMBER_DEFAULT):
        release_name = self.repo.name.lower()
        files = getHelmCharts(acr_details, port, release_name)
        for f in files:
            newFile = f.path
            content = f.content
            repo.create_file(
                path=newFile,
                message="Create file charts",
                content=content,
                branch="master",
            )
        print("charts pushed to repo for ")

    def chartsExist(self, repo):
        allFiles = None
        try:
            allFiles = repo.get_contents("/charts")
        except GithubException as ex:
            print(ex)
            allFiles = None

        if allFiles != None and len(allFiles) > 0:
            print("Charts already exist")
            return True
        else:
            print("Charts don't exists")
            False

    def workFlowFileExists(self, repo):
        allFiles = None
        try:
            allFiles = repo.get_contents("/.github/workflows")
        except GithubException as ex:
            print(ex)
            allFiles = None

        if allFiles != None and len(allFiles) > 0:
            print("Workflows already exist")
            return True
        else:
            print("Workflows don't exists")
            return False

    def pushWorkFlow(self, repo, cluster_details, acr_details):
        workflow_files = get_yaml_template_for_repo(
            cluster_details, acr_details, repo.name)
        print("workflow pushed to repo for %s" % (repo.name))
        returnCommit = None
        for single_file in workflow_files:
            print("file path: %s" % (single_file.path))
            print("file content: %s" % (single_file.content))
            returnCommit = repo.create_file(
                path=single_file.path,
                message="Create workflows",
                content=single_file.content,
                branch="master",
            )
        return returnCommit

    def cleanChartsFolder(self, repos):
        print(" cleaning up charts folder")
        allFiles = repos.get_contents("/charts")
        for f in allFiles:
            values = repos.get_contents(f.path)
            if not type(values) == list:
                sha = values.sha
                if f.path.startswith("charts"):
                    repos.delete_file(
                        path=f.path,
                        message="Delete file for testDeleteFile",
                        sha=sha,
                        branch="master",
                    )

        allFiles = repos.get_contents("/charts/templates")
        for f in allFiles:
            values = repos.get_contents(f.path)
            if not type(values) == list:
                sha = values.sha
                if f.path.startswith("charts"):
                    print("deleting templates")
                    repos.delete_file(
                        path=f.path,
                        message="Delete file for testDeleteFile",
                        sha=sha,
                        branch="master",
                    )

    def pushdummyFiles(self, repo):
        f = open("azdevopsdemo.pkl", "rb")
        data = f.read()
        f.close()

        commit = None
        contents = repo.get_contents("/azdevopsdemo.pkl")
        if not str(contents.content) == str(data):
            commit = repo.update_file(path=contents.path, message="updating pkl file",
                                      content=data, sha=contents.sha, branch="master")
            print("pkl file committed")
            print(commit)
        else:
            print("Nothing to commit for pkl file")
        return commit

    def pushFiles(self, repo):
        f = open("azdevopsdemo.pkl", "rb")
        data = f.read()
        f.close()

        commit = None

        try:
            
            modelUploadScript = open('modelUpload.py')
            exec(modelUploadScript.read())
            modelUploadScript.close()
            print("model uploaded successfully");
        except:
            print(" error while uploading a model")


        # contents = repo.get_contents("/azdevopsdemo.pkl")
        # if not str(contents.content) == str(data):
        #     commit = repo.update_file(path=contents.path, message="updating pkl file",
        #                               content=data, sha=contents.sha, branch="master")
        #     print("pkl file committed")
        #     print(commit)
        # else:
        #     print("Nothing to commit for pkl file")

        remoteNotebookContent = repo.get_contents(
            "/SampleModelGeneratorScriptCopy.ipynb")
        localNotebookContent = get_file_content(
            "SampleModelGeneratorScriptCopy.ipynb")
        print(localNotebookContent)
        if not remoteNotebookContent.content == localNotebookContent:
            commit = repo.update_file(path=remoteNotebookContent.path, message="updating notebook file",
                                      content=localNotebookContent, sha=remoteNotebookContent.sha, branch="master")
            print("notebook file committed")
            print(commit)
        else:
            print("Nothing to commit for pkl file")
        return commit

    def commitAppFile(self):
        # get the app path, then scan the file and then update it .
        print(abspath(os.curdir))
        ct = get_file_content("app.py")
        print(ct)

        appFile = self.repo.get_contents("/app.py")
        if not type(appFile) == list:
            print(appFile.sha)

    def getWorkflowStatus(self, commit_sha, cluster_details):
        repo = self.getRepo()
        check_run_id = get_work_flow_check_runID(
            repo.name, repo.owner.login, commit_sha, self.patToken)
        print(check_run_id)
        workflow_url = 'https://github.com/{owner}/{repo_id}/runs/{checkID}'.format(owner=repo.owner.login, repo_id=repo.name,
                                                                                    checkID=check_run_id)
        print('GitHub Action workflow has been created - {}'.format(workflow_url))

        configure_aks_credentials(
            cluster_details['name'], cluster_details['resourceGroup'])

        release_name = repo.name.lower()
        deployment_ip, port = get_deployment_IP_port(release_name, "python")
        deployUrl = 'http://{ip}:{port}/predict'.format(
            ip=deployment_ip, port=port)
        print(json.dumps({"deployUrl": deployUrl}))
        # print("Checking run status")
        check_run_status, check_run_conclusion = poll_workflow_status(
            repo.name, repo.owner.login, check_run_id, self.patToken)

        print(" workflow completed : ")
        print("check_run_status " + str(check_run_status))
        print("check_run_conclusion " + str(check_run_conclusion))

    def createRepoSecret(self, repoObj, secret_name, secret_value):
        """
        repo should be repository full name like {username}/{repo_name} : shpraka/testmlrepo
        # create-or-update-a-secret-for-a-repository
        API Documentation - https://developer.github.com/v3/actions/secrets/
        """
        repo = repoObj.owner.login + "/" + repoObj.name
        if not self.checkIfSecretExists(repo, secret_name):
            token = self.patToken
            headers = get_application_json_header()
            key_details = self.getPublicKey(repo)
            encrypted_text = encrypt_secret(key_details['key'], secret_value)
            # Remove the additional new lines added by encoder
            encrypted_text = encrypted_text.replace('\n', '')
            create_secre_request_body = {
                "encrypted_value": encrypted_text,
                "key_id": key_details['key_id']
            }
            create_secrets_url = 'https://api.github.com/repos/{repo}/actions/secrets/{secret_name}'.format(
                repo=repo, secret_name=secret_name)
            response = requests.put(create_secrets_url, auth=(
                '', token), json=create_secre_request_body, headers=headers)
            print(response)

    def getPublicKey(self, repo):
        """
        API Documentation - https://developer.github.com/v3/actions/secrets/#get-your-public-key
        """
        get_public_key_url = 'https://api.github.com/repos/{repo}/actions/secrets/public-key'.format(
            repo=repo)
        get_response = requests.get(
            get_public_key_url, auth=('', self.patToken))
        key_details = get_response.json()
        return key_details

    def checkIfSecretExists(self, repoFullName, secret_name):
        get_secrets_url = 'https://api.github.com/repos/{repo}/actions/secrets'.format(
            repo=repoFullName, secret_name=secret_name)
        get_response = requests.get(
            get_secrets_url, auth=('', self.patToken))
        secretResponse = get_response.json()
        if len(secretResponse['secrets']) > 0:
            for secret in secretResponse['secrets']:
                if secret['name'] == secret_name:
                    return True
        return False
