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
#url forma
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

