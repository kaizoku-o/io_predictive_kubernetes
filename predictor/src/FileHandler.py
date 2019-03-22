from pandas import read_csv
from BaseDataHandler import BaseDataHandler

class FileHandler(BaseDataHandler):
	fileName_ = ""

	def __init__(self, fileName):
		self.fileName_ = fileName		
		super().__init__()

	def get_data(self):
		return read_csv(self.fileName_, header=0, parse_dates=[0], 
			index_col=0).values

