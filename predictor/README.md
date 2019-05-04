# Predictor Module
#### Author: Sohail Shaikh (sashaikh)

This folder contains the source code and build environment of Predictor module. We provide a REST-ful api interface for interaction with this module. The predictor module listens on the port 9580 so it is recommended to forward the port 9580 if you're testing the module from a remote machine.
To run or evaluate the accuracy of the algorithms I would recommend executing the jupyter notebooks in the predictor/src/eval directory. Further details about the jupyter notebooks can be found in the eval directory.

### Requirements
* docker
* build-essentials
* private docker repository
* Kubernetes deployment
* jupyter notebook (for evaluation only)

#### Algorithms
The Predictor module contains the following values:
* ARIMA
* Holt Winters
* Linear Regression (Implemented but not being used)
* Weighted Moving Average
* Exponential Smoothing (Implemented but not being used)

### Files

1. makefile - (sashaikh)
  	Running make builds the docker image and pushes it to your k8s deployment
    
2. dockerfile (sashaikh)
    1. instructions docker to make the tetris-predictor image.


## The Predictor module has the following directories:

1. predictor/src: (sashaikh)
 		This folder contains the various source files that are being used.
 		Also has a README.md that describes each of the files in predictor/src/

2. predictor/src/eval: (sashaikh)
		This folder contains the evaluations of our algorithms. It contains the jupyter notebooks as well as the datasets that are being used.  
		This also contains a README.md describing the evaluation files.  

