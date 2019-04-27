
### Files

1. main.py
    1. Contains the main scheduler source code

### Folders

1. helpers
    1.  Additional python files that help facilitate tetris ability to provision pods on nodes.

### Execution Sequence

1. Find a pending Pod
2. Find all nodes in the system
3. Ask Predicator for future workloads
4. Bind pod to a node with lowest future workload
    
