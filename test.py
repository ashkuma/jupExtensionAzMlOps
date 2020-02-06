from jupextdemo.utlis import *
from jupextdemo.githubHelper import *
from jupextdemo.azaks_deploy import *
def _test_accounts():
    pass


replyObject = {};
if __name__ == "__main__":
    #_test_accounts()
    #isValidRepoForPat()
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
    

    print(replyObject)

    

    
    