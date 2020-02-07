from jupextdemo.utlis import *
from jupextdemo.githubHelper import *
from jupextdemo.azaks_deploy import *
def _test_accounts():
    pass





replyObject = {};
if __name__ == "__main__":
    # STEP 1 : take the AKS and ACR details
    # STEP 2 : Configure the Workflow files if they don't exist
    # STEP 3:  Check-In the Workflow files to Github Repo

    aks_dep = AKSDeploy();
    if aks_dep.IsUserLoggedIn() :
        replyObject["DefaultSubscription"] = aks_dep.getDefaultSubscription()
    else:
        aks_dep.loginUserFlow()
        replyObject["DefaultSubscription"] = aks_dep.getDefaultSubscription() 

    # get ACR details
    replyObject["ACRAccount"] = aks_dep.getACRDetails()

    # get AKS details
    replyObject["AKSCluster"] =  aks_dep.getAKSDetails()
    

    # print(replyObject)

    # now use this object and pass it to Github manager to implement 

    gm = GithubManager("")
    gm.pushDeployFilestoRepo(replyObject["AKSCluster"],replyObject["ACRAccount"])
        

    # # print(files)
    # newFile = "charts/Chart.yml"
    # content = "Hello world".encode()
    # repos.create_file(
    #     path=newFile,
    #     message="Create file for testCreateFile",
    #     content="this is the file content",
    #     branch="master",
    # )


    

    

    
    