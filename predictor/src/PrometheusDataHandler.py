from BaseDataHandler import BaseDataHandler
from prometheusQueries import Queries
from prometheusUtils import run_query_range

class PrometheusDataHandler(BaseDataHandler):
	def __init__(self):
		super().__init__()

	def get_data():
		return run_query_range(Queries["cpu"], 1552290000, 1552320000, 60)