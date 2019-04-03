import requests
import json
from PrometheusDataHandler import PrometheusDataHandler
from FileHandler import FileHandler
from Predictor import Predictor

class RequestResponseHandler:
	def __init__(self, apiName):
		self.data_ = {}
		self.apiName_ = apiName

	apiName_ = ""

	# encode a json object and return it
	def encode(self, request):
		pass

class AccuracyHandler(RequestResponseHandler):
	def __init__(self):
		super().__init__('getAccuracy')

	def process(self, request):
		model = request['model']
		pdHandler = PrometheusDataHandler(model)
		data = pdHandler.get_data()

		pred = Predictor()
		for ip in data:
			values = data[ip]
			self.data_[ip] = pred.accuracy(values)

	def encode(self, request):
		accuracy = {}
		metric = {}
		accuracy['accuracy'] = self.data_
		metric['metric'] = 'rmse'

		jsonList = []
		jsonList.append(accuracy)
		jsonList.append(metric)

		lst = []
		lst.append(jsonList)

		json_data = json.dumps(lst)
		return json_data

class WorkloadPredictionHandler(RequestResponseHandler):
	def __init__(self):
		self.data_ = {}
		super().__init__('predictWorkload')

	def process(self, request):
		model = request['model']
		pdHandler = PrometheusDataHandler(model)
		data = pdHandler.get_data()
		
		# Example of using a fileHandler
		# csv_values = FileHandler('../data/exchange.csv').get_data()
		# prediction = pred.arima(csv_values[0:-1-i], 1+i)

		for ip in data:
			# values is a tuple (time, workload)
			values = data[ip]
			pred = Predictor()
			prediction = pred.get_prediction(values)
			self.data_[ip] = prediction[-1]

	# encode a json response
	def encode(self, request):
		workload = {}
		workloadType = {}
		workloadUnit = {}

		workload['workload'] = self.data_
		workloadType['workloadType'] = request['model']
		workloadUnit['unit'] = 'percent'

		jsonList = []
		jsonList.append(workload)
		jsonList.append(workloadType)
		jsonList.append(workloadUnit)

		lst = []
		lst.append(jsonList)

		json_data = json.dumps(lst)
		return json_data