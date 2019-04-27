#!/usr/bin/env python3

from kubernetes import client,config,watch
from os import environ as ENV
from helper.PrometheusNodeSelector import PrometheusNodeSelector as pns
from kubernetes.client.rest import ApiException
from helper.GenericStatsCollector import GenericStatsCollector
from helper.SchedulerDecorator import backoff
import helper.logit as logit

__author__ = "Kyle Martin (kdmarti2)"


logging = logit.get_logger()
##
#Globals
##

##
#Set by the environment
#Tetris Scheduler Lookup String
##
scheduler_cpu = None
scheduler_mem = None
scheduler_io = None

##
#Set By The Environment
#Determine which Namespace that tetris looks at for pending pods
##
namespace = None

##
#PrometheusNodeSelector Object Class that handles the contacting of Prometheus
#and seleting which node has the lowest predicted workload
##
cpu_model = None
mem_model = None
IO_model = None

##
#Object Class to interact with Kubernetes
##
v1_api = None

##
#End of Globals
##


##
#@Ret String get_nodes(p object)
#This function will first query for all available and ready nodes in the K8s cluster
#Determine the internal IP address of these nodes and associate this internal IP address
#to the DNS name that K8s will use.  When need this association because Prometheous uses
#IPaddress to identify seperate nodes not DNS names like how K8s does it.  This allows
#me to have K8s and prometheous talk the same language.  Once this dictionary is filled
#call node_selection to select a node to place a container on.
##
def get_nodes(p):
    logging.info("Getting Nodes")

    ready_nodes = {}
    ##
    #Step 2 - Getting a list of ready nodes
    ##
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
#@backoff - See SchedulerDecorator.py
#This is to prevent wasted time and effort on scheduling a pod that has already been scheduled
#Also used to handle weird Error handing case
#
#Scheduler(string,Object,String)
#@name - name represents the name of the pod to provision onto a node
#@model - which node selector to use to determine the node with least predicitive workload
#@ns - namespace that the pod to be provisioned is in
##
@backoff
def scheduler(name,model,ns):

    ##
    #Step 3 - Selecting a node
    ##
    node = get_nodes(model)
    logging.info("Putting {0} on {1} in namespace: {2}".format(name,node,ns))
    
    #
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
    #Step 4 - Bind the pod to a node
    #Finished
    ##
    return v1_api.create_namespaced_binding(namespace=ns,body=body)

##
#@init - function sets the globals and retrieves configuration environmen variables
#at startup.
##
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

##
#@main - Function runs Forever to find new pods to provision on availale K8s Nodes
##
#Citation: https://sysdig.com/blog/kubernetes-scheduler/
#The following link was usd great guide to extract the four steps in making a Kubernetes scheduler.
##
def main():
    init();

    logging.basicConfig(level=logging.INFO)
    logging.info("Starting to Schedular pods for Tetris in namespace: {0}".format(namespace))
    w = watch.Watch()

    ##
    #Step 1 - Find a pod in a pending state
    #
    #Only provision pods that wants to use our scheduler
    #tetris-scheduler-cpu
    #tetris-scheduler-io
    #tetris-scheduler-mem
    ##
    while True:
        for event in w.stream(v1_api.list_namespaced_pod,namespace):
            logging.info("Event Triggered. Phase: {0} scheduler_name: {1}".format(event['object'].status.phase,event['object'].spec.scheduler_name))
            if event['object'].status.phase == "Pending":
                    
                if event['object'].spec.scheduler_name == scheduler_cpu:
                    scheduler(event['object'].metadata.name,model_cpu,namespace)
                elif event['object'].spec.scheduler_name == scheduler_mem:
                    scheduler(event['object'].metadata.name,model_mem,namespace)
                elif event['object'].spec.scheduler_name == scheduler_io:
                    scheduler(event['object'].metadata.name,model_io,namespace)


if __name__ == '__main__':
    main()
