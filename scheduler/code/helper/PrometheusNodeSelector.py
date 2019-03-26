from .GenericNodeSelector import GenericNodeSelector
from .PrometheusQuery import get_predict_workload

import sys
import json

class PrometheusNodeSelector(GenericNodeSelector):
    def __init__(self,alg,api,log_collector=None):
        self.alg = alg;
        self.api = api;
        self.log_collector = log_collector;
        super().__init__()

    def node_selection(self,nodeList: dict) -> str:
        if len(nodeList.values()) == 0:
            raise RuntimeError("No Nodes To select From")
        else:
            node_workloads = get_predict_workload(self.api,self.alg)
            for node_ip in node_workloads:
                try:
                    ip = node_ip[0].split(':')[0]
                    msg = {
                        "Data" : node_workloads,
                        "Choice" : nodeList[ip]
                    }
                    print(msg);
                    sys.stdout.flush()
                    if self.log_collector:
                        self.log_collector.write_log(json.dumps(msg))
                    return nodeList[ip]
                except KeyError:
                    pass

            raise RuntimeError("Failed To select A Node")

