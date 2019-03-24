from requests import *

import json
import operator

#[
# [
#   {
#     “workload”: {
#       “192.168.0.2": 48.16889858462753,
#       “192.168.0.3”: 48.45593438604228
#     }
#   },
#   {
#     “workloadType”: “cpu”
#   },
#   {
#     “unit”: “percent”
#   }
# ]
#]

##
#url format 
##
def get_predict_workload(api: str,model: str,time:int = 60) -> dict:
    request_format = {
            "apiName" : "predictWorkload",
            "model" : model,
            "time" : time,
    }

    try:
        r = post(api,json=request_format)
        if r.status_code != 200:
            ##
            #Improve Error Handling Here
            ##
            raise RuntimeError("StatusCode {0}".format(r.status_ode))
        else:
            workloads = r.json()[0][0]["workload"]
            order_loads = sorted(workloads.items(),key=operator.itemgetter(1))
            return order_loads;
            
    except exceptions.ConnectionError:
        print("Failed to Connect")


print(get_predict_workload("http://127.0.0.1:9580/api","cpu"));


