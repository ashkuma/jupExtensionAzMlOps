from github import Github, GithubException
from .utils import *
from .githubHelper import *


class GithubManager():
    def __init__(self, patToken):
        self.patToken = patToken
        self.g = Github(self.patToken)

    def _getNewToken(self):
        return self.patToken

    def pushDeployFilestoRepo(self, cluster_details, acr_details):
        # 1 assume language as python
        # 2 assume we are in the same repo, from where is it invoking
        # 3 assuming user already has docker file
        # assuming helmCharts and
        repo = self.getRepo()
        if repo == None:
            print("PAT entered is not for the correct owner of this repository. Make sure you are in the repository and notebook is opened from that repo only. ")
            return
        print(repo.name)
        if not self.chartsExist(repo):
            self.pushCharts(repo, acr_details, "5000")

        if not self.workFlowFileExists(repo):
            self.pushWorkFlow(repo, cluster_details, acr_details)

        pass

    def getRepo(self):
        # TODO : check if this works when i am in any branch as well
        x = getLocalRepoUrl()
        for repo in self. g.get_user().get_repos():
            if compareUrls(x, repo.clone_url):
                return repo

        return None

    def pushTestFile(self):
        pass

    def pushCharts(self, repo, acr_details, port="5000"):
        print("charts pushed to repo for ")
        files = getHelmCharts(acr_details, port)

        for f in files:
            newFile = f.path
            content = f.content
            print(newFile)
            repo.create_file(
                path=newFile,
                message="Create file charts",
                content=content,
                branch="master",
            )

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
        print(cluster_details)
        for single_file in workflow_files:
            print("file path: %s" % (single_file.path))
            print("file content: %s" % (single_file.content))
            repo.create_file(
                path=single_file.path,
                message="Create workflows",
                content=single_file.content,
                branch="master",
            )
        pass

    def cleanChartsFolder(self, repos):
        print(" cleaning up charts folder")
        allFiles = repos.get_contents("/charts")
        for f in allFiles:
            print(f.path)
            values = repos.get_contents(f.path)
            if not type(values) == list:
                sha = values.sha
                print(sha)
                if f.path.startswith("charts"):
                    repos.delete_file(
                        path=f.path,
                        message="Delete file for testDeleteFile",
                        sha=sha,
                        branch="master",
                    )

        allFiles = repos.get_contents("/charts/templates")
        for f in allFiles:
            print(f.path)
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
            print(newFile)
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
