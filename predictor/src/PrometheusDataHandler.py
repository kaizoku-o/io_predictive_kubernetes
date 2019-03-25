from BaseDataHandler import BaseDataHandler
from prometheusQueries import Queries
from prometheusUtils import run_query_range

class PrometheusDataHandler(BaseDataHandler):
	def __init__(self, mode):
		self.mode_ = mode
		super().__init__()

	def get_data(self):
		result = []
		if (self.mode_ == "memory"):
			result = run_query_range(Queries["mem"], 1552290000, 1552320000, 60)
		else:
			result = run_query_range(Queries["cpu"], 1552290000, 1552320000, 60)
		# print(type(result))
		# print(result)
		hosts = {x[0] for x in result}
		response = {}
		for host in hosts:
			response[host] = ','.join([x[2] for x in result if x[0]==host])
		# print(response)
		return response