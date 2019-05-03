from requests import *

import json
import operator

##
#Function is used to ask the predicator for future workloads of a certain type
#String api -> location of the predicator api
#String model -> expected to be cpu, mem, or io.  Represents the workload to query about
#int time -> number of seconds to predict into the future
#return dict -> ordered dictionary were the first value will contain the node with the lowest predicted workload.
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
            raise RuntimeError("StatusCode {0}".format(r.status_code))
        else:
            workloads = r.json()[0][0]["workload"]
            order_loads = sorted(workloads.items(),key=operator.itemgetter(1))
            return order_loads;
            
    except exceptions.ConnectionError:
        raise RuntimeError("Failed to Connect")

