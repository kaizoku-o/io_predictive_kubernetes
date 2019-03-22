from RequestParser import RequestParser
from RequestResponseHandler import WorkloadPredictionHandler


# Create a RequestParserObject
requestParser = RequestParser()

# Register all handlers with requestParser
# Each handler will support an api
# Right now we will have only 1 api which is for predicting workloads
workLoadPred = WorkloadPredictionHandler()
requestParser.registerHandler(workLoadPred)

request = {'apiName':'predictWorkload'}
requestParser.parse(request);