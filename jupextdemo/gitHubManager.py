from github import Github
from .utlis import *

class GithubManager():
    def __init__(self,patToken):
        self.patToken = patToken;
        self.g = Github(self.patToken);

    def _getNewToken(self):
        return self.patToken

    def pushWorkFlow(self):
        # 1 assume language as python
        # 2 assume we are in the same repo, from where is it invoking
        # 3 assuming user already has docker file
        # assuming helmCharts and 
        pass

    def pushTestFile(self):
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

    def commitDocker(self):
        pass

    def commitWorkflow(self):
        pass

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


    
