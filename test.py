from jupextdemo.utlis import *
from jupextdemo.githubHelper import *
from jupextdemo.azaks_deploy import *
def _test_accounts():
    pass


replyObject = {};
if __name__ == "__main__":
    # #_test_accounts()
    # #isValidRepoForPat()
    # aks_dep = AKSDeploy();
    # if aks_dep.IsUserLoggedIn() :
    #     replyObject["DefaultSubscription"] = aks_dep.getDefaultSubscription()
    # else:
    #     aks_dep.loginUserFlow()
    #     replyObject["DefaultSubscription"] = aks_dep.getDefaultSubscription() 

    # # get ACR details
    # replyObject["ACRAccount"] = aks_dep.getACRDetails()

    # # get AKS details
    # replyObject["AKSCluster"] =  aks_dep.getAKSDetails()
    

    # print(replyObject)


    gm = GithubManager("e76551da10530f239c93038fa8902d97eec18ebc")
    repos = list(gm.g.get_user().get_repos())[0]
    # print(repos)
    files = getHelmCharts(None,None)
    allFiles = repos.get_contents("/")
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
        

    # # print(files)
    # newFile = "charts/Chart.yml"
    # content = "Hello world".encode()
    # repos.create_file(
    #     path=newFile,
    #     message="Create file for testCreateFile",
    #     content="this is the file content",
    #     branch="master",
    # )


    # for f in files :
    #     print(f.replace('\\','/'))
    #     newFile = f
    #     if newFile == "charts":
    #         continue
    #     content = "Hello world".encode()
    #     repos.create_file(
    #         path=newFile,
    #         message="Create file for testCreateFile",
    #         content="this is the file content",
    #         branch="master",
    #     )

    

    
    