from BaseDataHandler import BaseDataHandler
from prometheusQueries import Queries
from prometheusUtils import run_query_range
import time

class PrometheusDataHandler(BaseDataHandler):
	def __init__(self, mode):
		self.mode_ = mode
		super().__init__()

	def get_data(self):
		"""
		Fetch data from prometheus as required for training and prediction
		Arguments:
			Type of model: "cpu", "mem", "io"
		Returns:
			A dictionary of Node_IP -> list of tuples(time, workload)
		"""	
		end_time = int(time.time())
		hrs = 6
		start_time = end_time - 60*60*hrs

		# A map to link the model with appropriate query name
		query_map = {
			"cpu" : "cpu",
			"mem" : "mem_utilization_perc_100",
			"io" : "disk_io_explicit"
		}

		result = run_query_range(Queries[query_map[self.mode_]], start_time, end_time, 60)
		hosts = {x[0] for x in result}
		response = {}

		# Creating a final response which is a map of 
		for host in hosts:
			response[host] = [(int(x[1]), float(x[2])) for x in result 
							  if x[0]==host]
		return response