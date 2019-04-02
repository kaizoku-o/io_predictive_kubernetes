from BaseDataHandler import BaseDataHandler
from prometheusQueries import Queries
from prometheusUtils import run_query_range
import time

class PrometheusDataHandler(BaseDataHandler):
	def __init__(self):
		super().__init__()

	def get_data():
		"""
		Fetch data from prometheus as required for training and prediction
		Arguments:
			No arguments
		Returns:
			A dictionary of Node_IP -> list of tuples(time, workload)
		"""	
		end_time = int(time.time())
		hrs = 6
		start_time = end_time - 60*60*hrs

		result = run_query_range(Queries["cpu"], start_time, end_time, 60)
		hosts = {x[0] for x in result}
		response = {}

		# Creating a final response which is a map of 
		for host in hosts:
			response[host] = [(int(x[1]), float(x[2])) for x in result 
							  if x[0]==host]
		return response