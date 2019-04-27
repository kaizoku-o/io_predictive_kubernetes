### Predictor

#### Algorithms
* ARIMA
* Holt Winters
* Linear Regression
* Weighted Moving Average
* Exponential Smoothing

### Functions

#### prometheusQueries.py

Serves as a repository of the prometheus Queries used by the predictor module to query prometheus aganist. The queries are stored in the form of dictionary for easy access from other modules.

Each query has been documented for its purpose and its implementation details.
This module is used by **PrometheusDataHandler.py**.
