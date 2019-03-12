#!/usr/bin/env python3

import logging

from kubernetes import client,config,watch
from os import environ as ENV
from helper.PrometheusNodeSelector import PrometheusNodeSelector as pns

####################
#    READ ONLYS
####################
scheduler_name = ENV.get("SCHEDULER_NAME")
if "NAMESPACE" in ENV:
    namespace = ENV.get("NAMESPACE")
else
    namespace = "default"
############################
config.load_incluster_config()
v1_api = client.CoreV1Api()

def get_nodes():
    ready_nodes = {}
    for k8_node in v1_api.list_node().items:
        for status in k8_node.status.conditions:
            if status.status == "True" and status.type == "Ready":
                logging.info("Found Node {0} is Ready!".format(k8_node.metadata.name))
                ready_nodes[k8_node.metadata.name] = k8_node.status.pod_ip;
            else:
                logging.warning("Node {0} is not available".format(k8_node.metadata.name))
    
    return pns.node_selector(ready_nodes)

def scheduler(name,node,ns):
    logging.info("Putting {0} on {1} in namespace: {2}".format(name,node,ns))

def main():
    logging.info("Starting to Schedular pods for {0} in namespace: {1}".format(scheduler_name,namespace))
    watcher = watch.Watch()
    for event in w.stream(v1_api.list_namespaced_pod,namespace):
        if event['object'].status.phase == "Pending" and event['object'].spec.scheduler_name == schedular_name:
            ##
            #Kicks off the scheduling event
            ##
            schedular(event['object'].metadata.name,get_nodes(),namespace))

if __name__ == '__main__':
    main()
