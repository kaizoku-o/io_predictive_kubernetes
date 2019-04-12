from .GenericNodeSelector import GenericNodeSelector
from .PrometheusQuery import get_predict_workload

import sys
import json
import random
import logit

logging = logit.get_logger()

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
            logging.info(node_workloads);
            for node_ip in node_workloads:
                try:
                    ip = node_ip[0].split(':')[0]
                    msg = {
                        "Data" : node_workloads,
                        "Choice" : nodeList[ip]
                    }
                    logging.info(msg)
                    if self.log_collector:
                        self.log_collector.write_log(json.dumps(msg))
                    return nodeList[ip]
                except KeyError:
                    pass

            logging.info("Failed to get find Nodes"
            logging.info("Falling back to random selection");
            k8_nodes = nodeList.keys();
            if len(k8_nodes) > 1:
                selection = random.randint(0,len(k8_nodes)-1);
                return k8_nodes[selection]
            else:
                return k8_nodes[0]
