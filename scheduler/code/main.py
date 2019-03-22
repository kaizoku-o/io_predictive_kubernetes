#!/usr/bin/env python3

import logging

from kubernetes import client,config,watch
from os import environ as ENV
from helper.PrometheusNodeSelector import PrometheusNodeSelector as pns
from kubernetes.client.rest import ApiException


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
    ready_nodes = []
    for k8_node in v1_api.list_node().items:
        for status in k8_node.status.conditions:
            if status.status == "True" and status.type == "Ready":
                logging.info("Found Node {0} is Ready!".format(k8_node.metadata.name))
                ready_nodes.append(k8_node.metadata.name)
            else:
                logging.warning("Node {0} is not available".format(k8_node.metadata.name))
    
    return p.node_selection(ready_nodes)


##
#Might need Error handling by leveraging an error queue 
##
def scheduler(name,node,ns):
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
    #Needs Error handing here.
    #kubernetes.client.rest.ApiException
    ##
    #Its likely going to error due to a bug we can try catch it and ignore it
    ##
    try:
        v1_api.create_namespaced_binding(namespace=ns,body=body)
    except ApiException as e:
        logging.warning("Error has occured calling Create_namespaced_binding\n {0}\n".format(e));
    except ValueError as e:
        logging.warning("Recieved ValueError for Null target, Ignoring because https://github.com/kubernetes-client/python/issues/547#issuecomment-455362558\n")


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

    if "SCHEDULER_NAME" in ENV:
        scheduler_base = ENV.get("SCHEDULER_NAME")
    else:
        scheduler_base = "tetris-scheduler"
    
    
    scheduler_cpu = scheduler_base + "-cpu"
    scheduler_mem = scheduler_base + "-mem"
    scheduler_io = scheduler_base + "-io"

    model_cpu = pns("cpu")
    model_mem = pns("mem")
    model_io = pns("io")


    if "NAMESPACE" in ENV:
        namespace = ENV.get("NAMESPACE")
    else:
        namespace = "default"

    config.load_kube_config()
    v1_api = client.CoreV1Api()

def main():

    init();

    logging.basicConfig(level=logging.INFO)
    logging.info("Starting to Schedular pods for {0} in namespace: {1}".format("tetis",namespace))
    w = watch.Watch()

    while True:
        for event in w.stream(v1_api.list_namespaced_pod,namespace):
            logging.info("Event Triggered!!! Phase: {0} scheduler_name: {1}".format(event['object'].status.phase,event['object'].spec.scheduler_name))
            if event['object'].status.phase == "Pending":
                if event['object'].spec.scheduler_name == scheduler_cpu:
                    scheduler(event['object'].metadata.name,get_nodes(model_cpu),namespace)
                elif event['object'].spec.scheduler_name == scheduler_mem:
                    scheduler(event['object'].metadata.name,get_nodes(model_mem),namespace)
                elif event['object'].spec.scheduler_name == scheduler_io:
                    scheduler(event['object'].metadata.name,get_nodes(model_io),namespace)


if __name__ == '__main__':
    main()
