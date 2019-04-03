#!/usr/bin/env python3

import logging

from kubernetes import client,config,watch
from os import environ as ENV
from helper.PrometheusNodeSelector import PrometheusNodeSelector as pns
from kubernetes.client.rest import ApiException
from helper.GenericStatsCollector import GenericStatsCollector
from helper.SchedulerDeclators import backoff

##
#Globals
##

scheduler_cpu = None
scheduler_mem = None
scheduler_io = None

namespace = None

cpu_model = None
mem_model = None
IO_model = None

v1_api = None

##
#End of Globals
##


##
#Need To get the IP addresses
##

def get_nodes(p):
    logging.info("Getting Nodes!!!")

    ready_nodes = {}
    for k8_node in v1_api.list_node().items:
        for status in k8_node.status.conditions:
            if status.status == "True" and status.type == "Ready":
                for addr in k8_node.status.addresses:
                    if addr.type == 'InternalIP':
                        logging.info("Found Node {0}:{1} is Ready!".format(k8_node.metadata.name,addr.address))
                        ready_nodes[addr.address]= k8_node.metadata.name
                        break;
            else:
                logging.warning("Node {0} is not available".format(k8_node.metadata.name))

    return p.node_selection(ready_nodes)

##
#Might need Error handling by leveraging an error queue
#We need to use a decorator
##

@backoff
def scheduler(name,model,ns):

    node = get_nodes(model)

    logging.info("Putting {0} on {1} in namespace: {2}".format(name,node,ns))
    
    ##
    #Source: https://sysdig.com/blog/kubernetes-scheduler/
    ##

    ##
    #https://github.com/kubernetes-client/python/issues/547
    #https://github.com/kubernetes-client/python/issues/547#issuecomment-455362558
    ##

    target = client.V1ObjectReference()
    target.kind = "Node"
    target.apiVersion = "v1"
    target.name = node

    meta = client.V1ObjectMeta()
    meta.name = name
    body = client.V1Binding(target=target,metadata=meta)

    ##
    #Its likely going to error due to a bug we can try catch it and ignore it
    ##
    return v1_api.create_namespaced_binding(namespace=ns,body=body)


def init():
    ##
    #Globals
    ##
    global scheduler_cpu
    global scheduler_mem
    global scheduler_io

    global model_cpu
    global model_mem
    global model_io

    global namespace

    global v1_api

    prometheus_api = None;

    if "SCHEDULER_NAME" in ENV:
        scheduler_base = ENV.get("SCHEDULER_NAME")
    else:
        scheduler_base = "tetris-scheduler"

    if "PROMETHEUS_API" in ENV:
        prometheus_api = ENV.get("PROMETHEUS_API")
    else:
        prometheus_api = "http://127.0.0.1:9580/api";

    scheduler_cpu = scheduler_base + "-cpu"
    scheduler_mem = scheduler_base + "-mem"
    scheduler_io = scheduler_base + "-io"
    
    log_collector = GenericStatsCollector()

    model_cpu = pns("cpu",prometheus_api,log_collector)
    model_mem = pns("mem",prometheus_api,log_collector)
    model_io = pns("io",prometheus_api,log_collector)


    if "NAMESPACE" in ENV:
        namespace = ENV.get("NAMESPACE")
    else:
        namespace = "default"

    config.load_kube_config()
    v1_api = client.CoreV1Api()



def main():
    init();

    logging.basicConfig(level=logging.INFO)
    logging.info("Starting to Schedular pods for Tetris in namespace: {0}".format(namespace))
    w = watch.Watch()

    while True:
        for event in w.stream(v1_api.list_namespaced_pod,namespace):
            logging.info("Event Triggered!!! Phase: {0} scheduler_name: {1}".format(event['object'].status.phase,event['object'].spec.scheduler_name))
            if event['object'].status.phase == "Pending":
                    
                if event['object'].spec.scheduler_name == scheduler_cpu:
                    scheduler(event['object'].metadata.name,model_cpu,namespace)
                elif event['object'].spec.scheduler_name == scheduler_mem:
                    scheduler(event['object'].metadata.name,model_mem,namespace)
                elif event['object'].spec.scheduler_name == scheduler_io:
                    scheduler(event['object'].metadata.name,model_io,namespace)


if __name__ == '__main__':
    main()
