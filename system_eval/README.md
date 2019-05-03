## System Evaluation

This directory contains files and information about the experiments conducted for tetris and default scheduler.

```(bash)
.
├── IO
│   ├── exp1
│   ├── exp2
│   ├── exp3
│   ├── exp4
│   └── exp5
├── IOSTOCK
│   ├── exp1
│   ├── exp2
│   ├── exp3
│   ├── exp4
│   └── exp5
├── MEM
│   ├── exp1
│   ├── exp2
│   ├── exp3
│   ├── exp4
│   └── exp5
├── MEMSTOCK
│   ├── exp1
│   ├── exp2
│   ├── exp3
│   ├── exp4
│   └── exp5
├── __pycache__
├── data
│   ├── io
│   ├── mem
│   ├── old-sohail
│   ├── old-vasudev
│   └── original
├── plots
└── tester
```

Each experiment is run 5 times are the experiment results are recorded in the exp{1..5} directories as shown above.

Below is the description of individual directories

#### IO 
Experiments with Tetris IO scheduler.

#### MEM
Experiments with Tetris Memory scheduler.

#### IOSTOCK
Experiments with default scheduler for I/O intensive pods.

#### MEMSTOCK
Experiments with default scheduler for memory intensive pods.

#### data
Contains scripts and modules that are used for automated analysis of the generated experiment results. It also consists of previous experimental data

#### Analysis.py (kdmarti2, vabongal)
Analyzes the experiment results to obtain average values from 10k runs for each experiment.

#### output.txt (vabongal)
Raw intermediate data generated after parsing the responses from each of the 20 experiment results.

#### plots (vabongal)
All the plots are generated using Gnuplot. This directory contains the data files and the gnuplot source code to generate graphs in PNG format. 

#### tester (vabongal)
Includes scripts that are used to automate the experiment and evaluation steps. 
