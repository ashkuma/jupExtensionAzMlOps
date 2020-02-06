
import os
import sys
import subprocess
import json
from .gitHubManager import GithubManager


class AKSDeploy():
    def __init__(self):
        self.currentSubscription = None
        self.CurrentACR = None;
        self.CurrentAKS = None;
        self.UserLoggedIn = False
        self.azResourceHelper = AKSDeploy_ResourceHelper();
        self.azResourceCreator = AKSDeploy_ResourceCreator();

    def IsUserLoggedIn(self):
        if self.UserLoggedIn == True:
            return True

        # if cache value is not set , then do a test and reset the cache inside the object can be used later.
        try:
            accountsList = self.getUserAccountList()
            if len(accountsList) == 0:
                self.UserLoggedIn = False
                
            else:
                self.UserLoggedIn = True;
                
        except:
            self.UserLoggedIn=False
            
        return self.UserLoggedIn;

    def getUserAccountList(self):
        accountsList = subprocess.check_output("az account list -o json", shell=True)

        return json.loads(accountsList)


    def loginUserFlow(self):
        try:
            loginOutput = subprocess.check_output("az login")
            print(loginOutput)
            #TODO : This is a bug, here check the output when user didn't complete the login
            self.UserLoggedIn = True
        except:
            self.UserLoggedIn = False
            print("cloud not autehnticate user")

    def getDefaultSubscription(self):
        accountsList = json.loads(subprocess.check_output("az account list -o json", shell=True))
        s={}
        for acc in accountsList :
            if acc["isDefault"]:
                s[acc['id']]=acc["name"]
                self.currentSubscription = acc['id']
        
        return s

    def getResourceGroup(self):
        return self.azResourceHelper.getResourceGroup(self.currentSubscription)

    def getACRDetails(self):
        return self.azResourceHelper.getACRDetails(self.currentSubscription)

    def getAKSDetails(self):
        return self.azResourceHelper.getAKSDetails(self.currentSubscription)

class AKSDeploy_ResourceHelper():
    def __init__(self):
        pass
    def getResourceGroup(self,subscription):
        group_list = subprocess.check_output('az group list --subscription {subscription} -o json'.format(subscription=subscription), shell=True)
        group_list = json.loads(group_list)
        return group_list

    def getACRDetails(self,subscription):
        acr_list = subprocess.check_output('az acr list --subscription {subscription} -o json'.format(subscription=subscription), shell=True)
        acr_list = json.loads(acr_list)
        return acr_list

    def getAKSDetails(self,subscription):
        aks_list = subprocess.check_output('az aks list --subscription {subscription} -o json'.format(subscription=subscription), shell=True)
        aks_list = json.loads(aks_list)
        return aks_list


class AKSDeploy_ResourceCreator():
    def __init__(self):

        pass
    def createNewACR(self,registry_name, resource_group, sku='Basic'):
        try:
            acr_create = subprocess.check_output(
                ('az acr create --name {acr_name} --sku {sku} -g {group_name} -o json')
                .format(acr_name=registry_name, sku=sku, group_name=resource_group), shell=True)
            acr_create = json.loads(acr_create)
            return acr_create
        except Exception as ex:
            print(ex)

    def createNewAks(self,cluster_name,resource_group):
        try:
            aks_create = subprocess.check_output(('az aks create --name {cluster_name} -g {group_name} -o json').format(
                cluster_name=cluster_name, group_name=resource_group), shell=True)
            aks_create_json = json.loads(aks_create)
            return aks_create_json
        except Exception as ex:
            print(ex)
            pass

    def setCurrentACR(self,acrName):
        pass
    def setCurrentAKS(self,acrName):
        pass
    

        