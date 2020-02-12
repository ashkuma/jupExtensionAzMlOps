from github import Github, GithubException
from .utils import *
from .githubHelper import *


class GithubManager():
    def __init__(self, patToken):
        self.patToken = patToken
        self.g = Github(self.patToken)
        self.repo = None

    def _getNewToken(self):
        return self.patToken

    def pushDeployFilestoRepo(self, cluster_details, acr_details):
        # 1 assume language as python
        # 2 assume we are in the same repo, from where is it invoking
        # 3 assuming user already has docker file
        # assuming helmCharts and
        repo = self.getRepo()
        returnCommit = None
        if repo == None:
            print("PAT entered is not for the correct owner of this repository. Make sure you are in the repository and notebook is opened from that repo only. ")
            return
        if not self.chartsExist(repo):
            self.pushCharts(repo, acr_details, "5000")

        if not self.workFlowFileExists(repo):
            returnCommit = self.pushWorkFlow(
                repo, cluster_details, acr_details)
            print(returnCommit['commit'].sha)
            self.getWorkflowStatus(returnCommit['commit'].sha)

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

    def pushCharts(self, repo, acr_details, port="5000"):
        files = getHelmCharts(acr_details, port)
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

    def commitHelmCharts(self, repos):
        files = getHelmCharts(None, None)
        for f in files:
            f = f.replace('\\', '/')
            newFile = f
            if newFile == "charts":
                continue
            content = "Hello world".encode()
            repos.create_file(
                path=newFile,
                message="Create file for testCreateFile",
                content="this is the file content",
                branch="master",
            )

    def commitPKLFile(self):
        pass

    def commitAppFile(self):
        pass

    def getWorkflowStatus(self, commit_sha):
        repo = self.getRepo()
        check_run_id = get_work_flow_check_runID(
            repo.name, repo.owner.login, commit_sha, self.patToken)
        print(check_run_id)
        workflow_url = 'https://github.com/{repo_id}/runs/{checkID}'.format(repo_id=repo.name,
                                                                            checkID=check_run_id)
        print('GitHub Action workflow has been created - {}'.format(workflow_url))

        check_run_status, check_run_conclusion = poll_workflow_status(
            repo.name, repo.owner.login, check_run_id, self.patToken)

        print(" workflow completed : ")
        print("check_run_status " + str(check_run_status))
        print("check_run_conclusion " + str(check_run_conclusion))

        # configure_aks_credentials(cluster_details['name'], cluster_details['resourceGroup'])
        # deployment_ip, port = get_deployment_IP_port(RELEASE_NAME, language)
        # print('Your app is deployed at: http://{ip}:{port}'.format(ip=deployment_ip, port=port))

    def createRepoSecret(self, repo, secret_name, secret_value):
        """
        repo should be repository full name like {username}/{repo_name} : shpraka/testmlrepo
        API Documentation - https://developer.github.com/v3/actions/secrets/#create-or-update-a-secret-for-a-repository
        """
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
