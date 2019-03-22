from statsmodels.tsa.arima_model import ARIMA

class Predictor:
	model_list_ = []

	def __init__(self):
		pass
		
	def arima(self, csv_values, lookahead_window=1):
		p = 5# lag observations
		d = 1# degree of differencing
		q = 0# order/size of moving average
		X_Train = [x for x in csv_values]
		X_Train_len = len(csv_values)		
		prediction = 0
		for i in range(lookahead_window):
			model = ARIMA(X_Train, order=(p, d, q))
			model_fit = model.fit(disp = 0)
			model_fit = model.fit(disp = 0)
			prediction = model_fit.forecast()[0]
			X_Train.append(prediction)

		self.model_list_.append(model_fit)
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


