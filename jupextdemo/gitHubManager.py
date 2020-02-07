from github import Github
from .utlis import *
from .githubHelper import *


class GithubManager():
    def __init__(self,patToken):
        self.patToken = patToken;
        self.g = Github(self.patToken);

    def _getNewToken(self):
        return self.patToken


    def pushDeployFilestoRepo(self,cluster_details, acr_details):
        # 1 assume language as python
        # 2 assume we are in the same repo, from where is it invoking
        # 3 assuming user already has docker file
        # assuming helmCharts and 
        repo = self.getRepo()
        if repo == None:
            print("PAT entered is not for the correct owner if this repository. Make sure you are in the repository and notebook is opened from that repo only. ")
            return
        print(repo.name)
        if not self.chartsExist(repo):
            self.pushCharts(repo, acr_details, 5000)

        if not self.workFlowFileExists(repo):
            self.pushWorkFlow(repo,cluster_details, acr_details)

        pass

    def getRepo(self):
        # TODO : check if this works when i am in any branch as well
        x = getLocalRepoUrl()
        for repo in self. g.get_user().get_repos():
            if compareUrls(x,repo.clone_url):
                return repo
            
        return None
                
    def pushTestFile(self):
        pass

    def pushCharts(self,repo, acr_details, port=5000):
        print("charts pushed to repo for ")
        print(acr_details)
        pass

    def chartsExist(self,repo):
        pass

    def workFlowFileExists(self,repo):
        pass

    def pushWorkFlow(self,repo,cluster_details, acr_details):
        print("workflow pushed to repo for ")
        print(cluster_details)
        pass

    def cleanChartsFolder(self,repos):
        allFiles = repos.get_contents("/charts")
        for f in allFiles:
            print(f.path)
            values = repos.get_contents(f.path);
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

    def commitHelmCharts(self,repos):
        files = getHelmCharts(None,None)
        for f in files :
            f = f.replace('\\','/')
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


    
