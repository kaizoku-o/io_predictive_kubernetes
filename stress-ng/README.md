# Stress-ng
#### Author: Sohail Shaikh (sashaikh)

This folder contains the source code and build environment of workload stressors. 

There are 3 yaml deployment files:
cpu-stressor.yaml
mem-stressor.yaml
io-stressor.yaml

There is also a script mem-run.sh which start stress-ng. This script takes 

mem-run.sh:
1. Has a Dockerfile for creating a stress-ng container. Entry point is /usr/bin/stress-ng
2. The deployment files pull the docker image from caffiendd's repository. 
3. It accepts a command line argument: "mem", "cpu" or "io" and starts workload in the specified mode.

To run create the stressor:
1. Install docker and kubernetes
2. Run make
3. Deploy the specific container.
eg. kubectl create -f cpu-stressor.yaml
