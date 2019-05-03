### Tester

This directory contains files used to automate experiment and evaluations.

#### run_experiment.sh (vabongal)
Runs the experiment for a set of configs. It can run an entire experiment for stock/tetris with iteration number of the experiment. 

#### unit-test-tetris-predictor.sh (vabongal)
Checks if the tetris-predictor is available and is responding within a reasonable time so that the experiments can proceed. 

#### tester.py (kdmarti2)
Runs the actual experiment - Executes 10000 reads and writes to a database pod running in either of the kubernetes nodes. It connects to the first available database pod. 

#### dockerfile (kdmarti2)
Dockerfile to create container to install the tester module.

#### Makefile (kdmarti2)
Makefile to launch the test/run the experiment when requested.