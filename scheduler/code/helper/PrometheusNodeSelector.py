from .GenericNodeSelector import GenericNodeSelector
from .PrometheusQuery import get_predict_workload
class PrometheusNodeSelector(GenericNodeSelector):
    def __init__(self,alg,api):
        self.alg = alg;
        self.api = api;
        super().__init__()

    def node_selection(self,nodeList: dict) -> str:
        if len(nodeList.values()) == 0:
            raise RuntimeError("No Nodes To select From")
        else:
            node_workloads = get_predict_workload(self.api,self.alg)
            for node_ip in node_workloads:
                try:
                    ip = node_ip[0].split(':')[0]
                    return nodeList[ip]
                except KeyError:
                    pass

            ##
            #TODO: BETTER ERROR HANDLING WHEN WE CAN NOT FIND A NODE
            ##
            raise RuntimeError("Failed To select A Node")
            ############################################
            #Entering random_selection
            ############################################

            




