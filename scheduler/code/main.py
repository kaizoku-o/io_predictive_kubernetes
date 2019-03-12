#!/usr/bin/env python3

import logging

from kubernetes import client,config,watch
from os import environ as ENV
from helper.PrometheusNodeSelector import PrometheusNodeSelector as pns

####################
#    READ ONLYS
####################
if "SCHEDULER_NAME" in ENV:
    scheduler_name = ENV.get("SCHEDULER_NAME")
else:
    scheduler_name = "tetris-scheduler"

if "NAMESPACE" in ENV:
    namespace = ENV.get("NAMESPACE")
else:
    namespace = "default"
############################
config.load_incluster_config()
v1_api = client.CoreV1Api()
p = pns()

def get_nodes():
    ready_nodes = []
    for k8_node in v1_api.list_node().items:
        for status in k8_node.status.conditions:
            if status.status == "True" and status.type == "Ready":
                logging.info("Found Node {0} is Ready!".format(k8_node.metadata.name))
                ready_nodes.append(k8_node.metadata.name)
            else:
                logging.warning("Node {0} is not available".format(k8_node.metadata.name))
    
    return p.node_selection(ready_nodes)

def scheduler(name,node,ns):
    logging.info("Putting {0} on {1} in namespace: {2}".format(name,node,ns))

def main():
    logging.basicConfig(level=logging.INFO)
    logging.info("Starting to Schedular pods for {0} in namespace: {1}".format(scheduler_name,namespace))
    w = watch.Watch()
    for event in w.stream(v1_api.list_namespaced_pod,namespace):
        if event['object'].status.phase == "Pending" and event['object'].spec.scheduler_name == scheduler_name:
            ##
            #Kicks off the scheduling event
            ##
            scheduler(event['object'].metadata.name,get_nodes(),namespace)

if __name__ == '__main__':
    main()
