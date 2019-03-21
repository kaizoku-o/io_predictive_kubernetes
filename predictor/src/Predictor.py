from statsmodels.tsa.arima_model import ARIMA
from sklearn.metrics import mean_squared_error as MeanSquaredError
from .FileHandler import FileHandler

class Predictor:
	def __init__(self):
		self
		
	def arima(csv_values):
		p = 3# lag observations
		d = 1# degree of differencing
		q = 0# order/size of moving average
		input = FileHandler.get_data()
		length = len(input)

		X_Train_len = int(length*0.9)
		X_Train = input[0:X_Train_len]
		model = ARIMA(X_Train, p, d, q)
		model_fit = model.fit(disp = 0)
		prediction = model_fit.predict()
		return prediction

	def linear_svm():
		pass

	def guassian_svm():
		pass

	# double exponential smoothing
	def des():
		pass

	# weighted moving average
	def wma():
		pass
		
	def linear_regression():
		pass

	def get_prediction(lookahead_window):
		pass


