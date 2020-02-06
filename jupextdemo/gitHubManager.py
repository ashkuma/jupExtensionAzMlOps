from github import Github

class GithubManager():
    def __init__(self,patToken):
        self.patToken = patToken;
        self.g = Github(self.patToken);

    def _getNewToken(self):
        return self.patToken

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


    
