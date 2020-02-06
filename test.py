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


    gm = GithubManager("")
    repos = list(gm.g.get_user().get_repos())[0]
    # print(repos)
    files = getHelmCharts(None,None)
    print(files)
    
        

    # # print(files)
    # newFile = "charts/Chart.yml"
    # content = "Hello world".encode()
    # repos.create_file(
    #     path=newFile,
    #     message="Create file for testCreateFile",
    #     content="this is the file content",
    #     branch="master",
    # )


    

    

    
    