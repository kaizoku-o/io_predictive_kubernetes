### Files

1. main.py (sashaikh)
    Contains the starting point for prediction.
    Has the Flask API end-point "predictWorkload"
    We instantiate the AsyncLoadBalance here which is a singleton class and a component of the Precompute module.

2. Predictor.py (sashaikh)
	Has the implementation of all the prediction algorithms.

3. RequestResponseHandler.py (sashaikh)
	The request response handler contains WorkloadPredictionHandler which takes the data from prometheus and invokes the Predictor::getPrediction() method.
	All the handlers have to be registered with RequestParser.

4. RequestParser.py (sashaikh)
	Gets request from main.py through Flask API.
	From the request it extracts the apiName and invokes the appropirate RequestResponseHandler registered with it.


5. AsyncLoadBalance.py (kdmarti2, sashaikh)
	This is the multithreaded model in the Precompute module. 
	It has the populateBestModel() method which populates the best 

6. SimpleLoadBalance.py (kdmarti2)
	Single threaded version for getting the best model. Not used by our code.

7. GenericLoadBalance.py (kdmarti2)
	Base class of AsyncLoadBalance and SimpleLoadBalance.

8. BaseDataHandler.py (sashaikh)
	Base class of RequestResponseHandler and FileHandler.

9. FileHandler.py (sashaikh)
	Class to handle files. Was tested initially but not being used right now.

10. install_cron_entry.sh (sashaikh)
	Install a cron entry in the docker container which calls the precompute_scheduler.sh every 5 minutes.

11. precompute_scheduler.sh (sashaikh)
	Triggers the precompute module.

12. PrometheusDataHandler.py (sashaikh, vabongal)
	This is the interface that talks to prometheus to fetch data and gets called by RequestResponeHandler and AsyncLoadBalance to get data from prometheus.

13. prometheusQueries.py (vabongal)
	Serves as a repository of the prometheus Queries used by the predictor module to query prometheus aganist. The queries are stored in the form of dictionary for easy access from other modules.
	This module is used by **PrometheusDataHandler.py**.

14. prometheusUtils.py (vabongal)
	Utility class for interaction with prometheus.

15. classdiagram.png
	The class diagram of Prediction module.

### Folders

1. eval
	This folder contains the evaluations of our algorithms. It contains the jupyter notebooks as well as the datasets that are being used.    
