from statsmodels.tsa.arima_model import ARIMA
import statsmodels.api as sm

class Predictor:
	model_list_ = []

	def __init__(self):
		pass
	
	def arima(self, values, law=1):
		p = 5 # lag observations
		d = 1 # degree of differencing
		q = 0 # order/size of moving average

		X_Train = [x[1] for x in values]

		for i in range(law):
			model = ARIMA(X_Train, order=(p, d, q))
			model_fit = model.fit(disp = 0)
			prediction = model_fit.forecast()[0]
			X_Train.append(prediction)

		return 	prediction

	def linear_svm(self, values):

		pass

	def guassian_svm():
		pass

	# double exponential smoothing
	def des():
		pass

	# weighted moving average
	def wma():
		pass
		
	def linear_regression(self, values, law=1):
		Y_Train = [x[1] for x in values] # dependent varaible
		X_Train = [x[0] for x in values] # independent variable

		# Training a linear regression model with Ordinary Least Squares Method
		# Generalized Least Squares (GLS) and Weighted Least Squares (WLS)
		# are other alternatives to OLS. However, in terms of accuracy
		# not much difference was seen. 
		model = sm.OLS(Y_Train, X_Train).fit()

		sampling_duration = X_Train[1] - X_Train[0]

		last_X_Train = X_Train[-1]

		# Getting the times at which the next values are to be predicted
		X_Pred = [last_X_Train + x * sampling_duration for x in range(law)]
		predictions = model.predict(X_Pred)
		print(X_Pred)
		return predictions

	def get_prediction(self, values, lookahead_window=1):
		return self.arima(values, lookahead_window)
