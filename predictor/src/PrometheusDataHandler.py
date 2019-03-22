from BaseDataHandler import BaseDataHandler
from prometheusQueries import Queries
from prometheusUtils import run_query_range

class PrometheusDataHandler(BaseDataHandler):
	def __init__(self):
		super().__init__()

	def get_data():
		result = run_query_range(Queries["cpu"], 1552290000, 1552320000, 60)
		hosts = {x[0] for x in result}
		response = {}
		for host in hosts:
			response[host] = ','.join([x[2] for x in result if x[0]==host])
		return response