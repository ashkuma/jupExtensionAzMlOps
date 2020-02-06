import os
import sys
import subprocess
import json




def getUserSubscriptionsList():
    accountsList = json.loads(subprocess.check_output("az account list -o json", shell=True))
    s={}
    for acc in accountsList :
        s[acc['id']]=acc["name"]
    
    print(s)





