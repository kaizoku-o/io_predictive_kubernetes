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
		super().__init__('predictWorkload')

	def process(self):
		# data = pdHandler.get_data()
		csv_values = FileHandler('../data/exchange.csv').get_data()
		pred = Predictor()
		prediction = pred.arima(csv_values[0:-1])
		print("actual: " + str(csv_values[-1]) + " prediction: " + str(prediction))

	# encode a json response
	def encode(self):
		pass