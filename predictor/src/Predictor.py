from statsmodels.tsa.arima_model import ARIMA
from statsmodels.tsa.api import ExponentialSmoothing, SimpleExpSmoothing
import statsmodels.api as sm
import numpy as np
from sklearn.svm import SVR
from sklearn.metrics import mean_squared_error
from math import sqrt
import logging

log_format='%(asctime)s - %(process)d - %(levelname)s - %(filename)s - %(funcName)s - %(message)s'
logging.basicConfig(filename='predictor.log', filemode='a', 
	format=log_format, level=logging.DEBUG)

def mean_absolute_percentage_error(y_true, y_pred): 
    y_true, y_pred = np.array(y_true), np.array(y_pred)
    return np.mean(np.abs((y_true - y_pred) / y_true)) * 100

class Predictor:
	model_list_ = []

	def __init__(self):
		pass
	
	# problems with this
	def arima(self, values, law=6):
		import warnings
		warnings.filterwarnings('ignore')
		p = 5 # lag observations
		d = 0 # degree of differencing
		q = 3 # order/size of moving average

		X_Train = [x[1] for x in values]

		predictions = []
		model = ARIMA(X_Train, order=(p, d, q))
		model_fit = model.fit()
		predictions.append(model_fit.forecast(steps=law)[0])
		return 	predictions[-1]

	def simple_exponential_smoothing(self, values, law=6):
		Y_Train = [x[1] for x in values]
		model = SimpleExpSmoothing(Y_Train).fit()
		predictions = model.forecast(law)
		return predictions

	# double exponential smoothing
	def holtWinters_des(self, values, law=1):
		import warnings
		warnings.filterwarnings('ignore')
		Y_Train = []
		for i in range(0, len(values), 6):
			Y_Train.append(values[i][1])

		model = ExponentialSmoothing(Y_Train, seasonal_periods=50, 
			seasonal='add').fit(use_boxcox=True)
		predictions = model.forecast(law)
		return predictions

	# weighted moving average
	def wma(self, values, law=6):
		values_win = values[-6:-1]
		Y_Train = np.array([x[1] for x in values_win])
		prediction = []

		for i in range(law):
			weights = np.arange(1, len(Y_Train) + 1)
			prediction.append(np.sum(Y_Train*weights)/sum(weights))
			Y_Train = np.append(Y_Train, [prediction])
		
		return prediction
		
	def linear_regression(self, values, law=6):
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

	def accuracy(self, values, split_percent = 90):
		"""
		Give the accuracy for a prediction algorithm
		Arguments:
			values: Tuple of X: Independent variable and
							 Y: Dependent variable 
		Returns:
			Root Mean Squared Error for a prediction algorithm
		"""	

		model_error_list = []

		train_samples = int(len(values)*split_percent/100)

		values_train = values[0:train_samples]
		values_test = values[train_samples:]
		test_samples = len(values_test)

		logging.debug("Length of training set is %f", train_samples)
		logging.debug("Predicting %f values", test_samples)

		y_true = [x[1] for x in values_test]

		try:
			y_pred = self.arima(values_train, len(values_test))
			# rmse = sqrt(mean_squared_error(y_true, y_pred))
			err = mean_absolute_percentage_error(y_true, y_pred)
			logging.debug('arima error percent: %f', err)
			model_error_list.append( (err, 'arima') )
		except:
			logging.error("Exception ocurred, error percent could not be determined"
				" for arima")

		try:
			y_pred = self.linear_regression(values_train, len(values_test))
			# rmse = sqrt(mean_squared_error(y_true, y_pred))
			err = mean_absolute_percentage_error(y_true, y_pred)
			logging.debug('linear regression error percent: %f', err)
			model_error_list.append( (err, 'linear_regression') )

		except:
			logging.error("Exception ocurred, error percent could not be" 
				" determined for linear regression")

		try:
			y_pred = self. simple_exponential_smoothing(values_train, 
						len(values_test))
			# rmse = sqrt(mean_squared_error(y_true, y_pred))
			err = mean_absolute_percentage_error(y_true, y_pred)
			logging.debug('simple exponential smoothing error percent: %f', err)
			model_error_list.append( (err, 'simple_exponential_smoothing') )

		except:
			logging.error("Exception ocurred, error percent could not be"
				" determined for simple_exponential_smoothing")


		try:
			y_pred = self.holtWinters_des(values_train, len(values_test))
			# rmse = sqrt(mean_squared_error(y_true, y_pred))
			err = mean_absolute_percentage_error(y_true, y_pred)
			logging.debug('Holt Winters ES error percent: %f', err)
			model_error_list.append( (err, 'holtWinters_des') )
		except:
			logging.error("Exception ocurred, error percent could not be" 
				" determined for holtWinters_des")


		try:
			y_pred = self.wma(values_train, len(values_test))
			rmse = sqrt(mean_squared_error(y_true, y_pred))
			logging.debug('wma error percent: %f', err)
			err = mean_absolute_percentage_error(y_true, y_pred)
			model_error_list.append( (err, 'wma') )
		except ValueError:
			logging.error("Exception ocurred, error percent could not be" 
				" determined for wma")

		return model_error_list

	def get_prediction(self, values, model, lookahead_window=6):
		from AsyncLoadBalance import AsyncLoadBalance
		prediction = []
		precomputeBestModel = AsyncLoadBalance.getInstance()

		bestModel = precomputeBestModel.getBestModel(model)
		print("bestModel is ", bestModel)
		logging.debug("Using bestModel %s", bestModel)
		predictionAlgo = getattr(self, bestModel)

		try:
			prediction = predictionAlgo(values, lookahead_window)
		except:
			logging.error("Exception ocurred so falling back to wma")
			prediction = self.wma(values)
		precompute.populateBestModel()
		return prediction
