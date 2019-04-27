### Configuration files

This directory contains various configuration files that are required for a specific functionality.

*tetris-pv-volume.yaml*
```(bash)
This is kubernetes configuration file that creates a persistent volume. The mount points provided by the pods are ephimeral. To be able to store the data generated from the pods (specifically from the tetris-scheduler), a persistent volume is created which is used by the pod via a persistent-volume-claim
```

*tetris-pv-volumeclaim.yaml*
```(bash)
This is a kubernetes configuration file that creates a persistent volume claim. It defines a claim with metadata about how much of a storage will be allocated/claimed from a given persistent volume.
```