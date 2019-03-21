from pandas import read_csv

class FileHandler(BaseDataHandler):
	def __init__(self):		
		super().__init__()

	def get_data():
		fileName = ""
		return read_csv(fileName, header=0, parse_dates=[0], index_col=0).values
