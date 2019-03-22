import requests
import json
from PrometheusDataHandler import PrometheusDataHandler as pdHandler
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

	def process(self):
		# data = pdHandler.get_data()
		csv_values = FileHandler('../data/exchange.csv').get_data()
		pred = Predictor()

		# dummy node ip values
		node_ip = ['192.168.0.2', '192.168.0.3']

		for i, ip in enumerate(node_ip):
			prediction = pred.arima(csv_values[0:-5], 5)
			self.data_[ip] = prediction[0]

		print("actual: " + str(csv_values[-1]) + " prediction: " + str(prediction))

	# encode a json response
	def encode(self):
		json_data = json.dumps(self.data_)
		return json_data