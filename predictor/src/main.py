from RequestParser import RequestParser
from RequestResponseHandler import WorkloadPredictionHandler

# Create a RequestParserObject
requestParser = RequestParser()

# Register all handlers with requestParser
# Each handler will support an api
# Right now we will have only 1 api which is for predicting workloads
workLoadPred = WorkloadPredictionHandler()
requestParser.registerHandler(workLoadPred)

from flask import Flask, request, jsonify
app = Flask(__name__)

@app.route('/api', methods=['GET', 'POST'])
def api():
    print (request.is_json)
    response = requestParser.process_request(request.get_json())
    return response

if __name__ == '__main__':
	app.run(host= '0.0.0.0', debug=True, port=9580)