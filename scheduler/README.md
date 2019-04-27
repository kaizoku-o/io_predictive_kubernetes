# K8s Tetris Scheduler
#### Author: Kyle Martin (kdmarti2)

This folder containers the source code and build environment of the Tetris scheduler.  Inorder to use the tetris scheduler it is recommend that a private docker repository is setup that is accessible to the Kubernetes deployment.  Also establishing portforwarding through ssh tunneling is recommended to push the tetris image to the docker private repository.  I recommend using the `LocalForward 4999 127.0.0.1:50000` command in your ssh config file that handles ssh connections to the private docker repository.

### Requirements

* docker
* build-essentials
* private docker repository
* Kubernetes deployment

### Files

1. makefile - (kdmarti2)
    1. make clean - used to remove tetris scheduler deployment from K8s
    1. make deploy - used to deploy tetris scheduler onto K8s
    1. make build - used to make a new tetris scheduler image
    1. make push - used to push the new tetris image to the private docker repository
    
2. dockerfile (kdmarti2)
    1. instructions docker to make the tetris image.
    
3. tetris.yml (kdmarti2)
    1. Tetris deployment instructions
    1. persistent volume additions (vabongal)
    
### Folders

1. code 
    1. Contains tetris source code

2. cfg
    2. Contains admin configuration file that tetris needs in order to communicate with the cluster
