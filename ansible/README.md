### Ansible Orchestration Files

This module provides all the necessary ansible scripts, templates and files that are required to setup the kubernetes and monitoring environment.

The files can be categorized into:
* Templates (Jinja)
* Ansible-playbooks (yaml)
* configuration files

#### Templates

*prometheus_yml_template.j2*
```(bash)
This template defines the prometheus configuration file that is installed to /etc/prometheus/prometheus.yml.
```

*prometheus.service_template.j2*
```(bash)
This template creates an system init into the prometheus host so that prometheus is enabled at the startup and persists even after system reboot.
```

*tetris-predictor_service.j2*
```(bash)
This template enables tetris-predictor flask api and its prediction algorithm code bundled into a docker container to start at reboot. Provides easy interface to pull the latest image from the private docker registry from the master and re-install the predictor module.
```

#### Ansible playbook files

*K8install.yml*

```(bash)
This playbook is the primary entry point to begin the environment setup. Based on the IP addresses or node information specified in the inventory.yml, the k8smaster, node and prometheus server are configured and corresponding services are started in the nodes.
```