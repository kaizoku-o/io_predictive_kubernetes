import requests
import json
from PrometheusDataHandler import PrometheusDataHandler
from FileHandler import FileHandler
from Predictor import Predictor

class RequestResponseHandler:
	def __init__(self, apiName):
		self.apiName_ = apiName

	apiName_ = ""

	# encode a json object and return it
	def encode(self):
		pass


class WorkloadPredictionHandler(RequestResponseHandler):
	def __init__(self):
		self.data_ = {}
		super().__init__('predictWorkload')

	def process(self, request):
		model = request['model']
		pdHandler = PrometheusDataHandler(model)
		data = pdHandler.get_data()

		for ip in data:
			# print(ip)
			# print("\n")
			# print(ip.find('localhost'))
			if (ip.find('localhost') != -1):
				continue
			csv_values = data[ip]
			# print(csv_values)
			pred = Predictor()
			prediction = pred.arima(csv_values)
			self.data_[ip] = prediction[0]
			# csv_values = None

		# csv_values = FileHandler('../data/exchange.csv').get_data()
		# pred = Predictor()
		# # dummy node ip values
		# node_ip = ['192.168.0.2', '192.168.0.3']

		# for i, ip in enumerate(node_ip):
		# 	prediction = pred.arima(csv_values[0:-1-i], 1+i)
		# 	self.data_[ip] = prediction[0]
		# print("actual: " + str(csv_values[-1]) + " prediction: " + str(prediction))

	# encode a json response
	def encode(self):
		workload = {}
		workloadType = {}
		workloadUnit = {}

		workload['workload'] = self.data_
		workloadType['workloadType'] = 'cpu'
		workloadUnit['unit'] = 'percent'

		jsonList = []
		jsonList.append(workload)
		jsonList.append(workloadType)
		jsonList.append(workloadUnit)

		lst = []
		lst.append(jsonList)

		json_data = json.dumps(lst)
		return json_data