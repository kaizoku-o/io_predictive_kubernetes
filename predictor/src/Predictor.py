from statsmodels.tsa.arima_model import ARIMA

class Predictor:
	model_list_ = []

	def __init__(self):
		pass
		
	def arima(self, csv_values):
		p = 3# lag observations
		d = 1# degree of differencing
		q = 0# order/size of moving average
		X_Train_len = len(csv_values)
		X_Train = csv_values[0:X_Train_len]
		model = ARIMA(X_Train, order=(p, d, q))
		model_fit = model.fit(disp = 0)

		self.model_list_.append(model_fit)
		prediction = model_fit.forecast()[0]
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

	# def get_prediction(lookahead_window):
	# 	pass


