## Tetris: Predictive Pod Placement Strategy for Kubernetes

> Kubernetes (K8s) when provisioning resources for containerized applications does not measure the current I/O workload of the target provisioning node. Such I/O-unaware scheduler could lead to multiple I/O intensive pods creating an I/O bottleneck. This project hopes to improve K8s ability to provide better resource management by introducing custom metrics, specifically I/O and memory usage statistics. We aim to achieve this by developing a custom system referred to as Tetris, which incorporates predictive algorithms to provide more resource-aware pod placements.

This repository has all the source code required for the setup and evaluation of Tetris kubernetes scheduler.

### ansible
Complete environment setup is done using Ansible. This directory contains the playbooks, templates and scripts that are used to setup the kubernetes cluster and the prometheus monitoring system.

### predictor
Includes all the logic and implementation of the Tetris-predictor module, which consists of prediction algorithms and Flask APIs exposed to listen on requests from Tetris-scheduler for workload predictions. 
It also contains the eval directory which has the real datasets from our workloads that we used for the evaluation of our algorithms and the Jupyter notebooks for each of the algorithms.

### prometheus-api
Implements APIs for querying prometheus for metrics data over prometheus native APIs. It interacts with predictor module to supply metrics requested for training instance. 

### scheduler
Implements Tetris-scheduler, a custom scheduler used with applications such as I/O, Memory,CPU stressors and MySQL application pod for predictive scheduling. 

### ssh_keys
Contains SSH keys used by project authors to connect and configure access to AWS instances for Kubernetes cluster.

### stress-ng
Includes scripts and applications that is used for workload generators.

### system_eval
All experimental data and results are stored in this directory, including the scripts to automate the experiment and the python module used to process the results. 
