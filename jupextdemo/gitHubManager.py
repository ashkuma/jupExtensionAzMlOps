from github import Github

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


    def commitDocker(self):
        pass

    def commitWorkflow(self):
        pass

    def commitHelmCharts(self):
        pass

    def commitPKLFile(self):
        pass

    def commitAppFile(self):
        pass


    
