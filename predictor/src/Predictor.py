from statsmodels.tsa.arima_model import ARIMA
from statsmodels.tsa.api import ExponentialSmoothing, SimpleExpSmoothing
import statsmodels.api as sm
import numpy as np
from sklearn.svm import SVR

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

	def linear_svr(self, values, law=1):
		Y_Train = [x[1] for x in values] # dependent varaible
		X_Train = [[x[0]] for x in values] # independent variable

		model = SVR(kernel='linear', C=100, gamma='auto').fit(X_Train,
					Y_Train)

		sampling_duration = X_Train[1][0] - X_Train[0][0]
		last_X_Train = X_Train[-1][0]

		# Getting the times at which the next values are to be predicted
		X_Pred = [[last_X_Train + x * sampling_duration] for x in range(law)]

		predictions = model.predict(X_Pred)

		return predictions

	def guassian_svr(self, values, law=1):
		Y_Train = [x[1] for x in values] # dependent varaible
		X_Train = [[x[0]] for x in values] # independent variable

		model = SVR(kernel='rbf', C=1, gamma='auto', epsilon=.1).fit(X_Train,
					Y_Train)

		sampling_duration = X_Train[1][0] - X_Train[0][0]
		last_X_Train = X_Train[-1][0]

		# Getting the times at which the next values are to be predicted
		X_Pred = [[last_X_Train + x * sampling_duration] for x in range(law)]

		predictions = model.predict(X_Pred)
		
		return predictions

	def simple_exponential_smoothing(self, values, law=1):
		Y_Train = [x[1] for x in values]
		model = SimpleExpSmoothing(Y_Train).fit()
		predictions = model.forecast(law)
		return predictions

	# double exponential smoothing
	def holtWinters_des(self, values, law=1):
		Y_Train = [x[1] for x in values]
		model = ExponentialSmoothing(Y_Train, seasonal_periods=20, 
			trend='add', seasonal='add').fit(use_boxcox=True)
		predictions = model.forecast(law)
		return predictions

	# weighted moving average
	def wma(self, values, law=1):
		Y_Train = np.array([x[1] for x in values])
		prediction = []

		for i in range(law):
			weights = np.arange(1, len(Y_Train) + 1)
			prediction.append(np.sum(Y_Train*weights)/sum(weights))
			Y_Train = np.append(Y_Train, [prediction])
		
		return prediction
		
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
		return predictions

	def get_prediction(self, values, lookahead_window=1):
		return self.wma(values, lookahead_window)
