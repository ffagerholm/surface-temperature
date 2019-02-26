import statsmodels.api as sm
from sklearn.base import BaseEstimator, RegressorMixin


class SARIMAXWrapper(BaseEstimator, RegressorMixin):
    """Sklearn wrapper for statsmodels SARIMAX models.
    Wrapper for statsmodels SARIMAX model to make it compatible with the scikit-learn API
    """
    def __init__(self, 
                 order=(1, 0, 0), 
                 seasonal_order=(0, 0, 0, 0), 
                 trend=None, 
                 measurement_error=False, 
                 time_varying_regression=False, 
                 mle_regression=True, 
                 simple_differencing=False, 
                 enforce_stationarity=True, 
                 enforce_invertibility=True, 
                 hamilton_representation=False, 
                 concentrate_scale=False,
                 freq=None):
        self.SARIMAX = sm.tsa.SARIMAX
        self.order = order
        self.seasonal_order = seasonal_order
        self.trend = trend
        self.measurement_error = measurement_error
        self.enforce_stationarity = enforce_stationarity
        self.enforce_invertibility = enforce_invertibility
        self.freq = freq
        
    def fit(self, X, y=None):
        """Fit the model to data.
        Instantiates a SARIMAX object with the parameters given in the
        class initialization and calls the fit fuction of that object.
        Stores the results of the call in a instance variable.
        """
        self.model_ = self.SARIMAX(endog=X,  
                                   order=self.order, 
                                   seasonal_order=self.seasonal_order,
                                   trend=self.trend,
                                   measurement_error=self.measurement_error,
                                   enforce_stationarity=self.enforce_stationarity,
                                   enforce_invertibility=self.enforce_invertibility,
                                   freq=self.freq)
        try:
            self.results_ = self.model_.fit()
        except ValueError as error:
            print(self.order, error)
    
    def predict(self, X):
        """Create a forecast of the length of X.
        Wraps the function SARIMAXResults.forecast(steps=1, **kwargs)
        """
        return self.results_.forecast(len(X))