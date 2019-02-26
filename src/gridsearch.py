from warnings import catch_warnings
from warnings import filterwarnings
import pandas as pd
import statsmodels.api as sm
from sklearn.base import BaseEstimator, RegressorMixin
from sklearn.model_selection import TimeSeriesSplit
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import mean_squared_error


def score_model(y_train, y_test, parameters, error_metric):
    with catch_warnings():
        filterwarnings("ignore")
        model = sm.tsa.ARIMA(endog=y_train, **parameters)
        model_fit = model.fit(transparams=False, disp=0)
    
    aic = model_fit.aic
    bic = model_fit.bic
    
    y_pred = model_fit.forecast(len(y_test))[0]
    
    error = error_metric(y_test, y_pred)
    
    return model_fit, error, aic, bic
    

def gridsearch_arima(data, n_test, param_configs, error_metric=mean_squared_error):
    train_data = data[:-n_test] 
    test_data = data[-n_test:]
    results = []
    
    for config in param_configs:
        model_fit, error, aic, bic = score_model(train_data, test_data, config, error_metric)
        results.append({'model_fit': model_fit, 'config': config, 
                        'error': error, 'AIC': aic, 'BIC': bic})
        
    return results



def main():
    monthly_deviations = pd.read_csv('../data/NASA_GISS_LOTI_long_format.csv', 
                                 index_col='Date', 
                                 parse_dates=['Date'])
    # take deviations from mean up to (and including) 2019-01
    global_deviations = monthly_deviations['global'][:'2019-01']

    param_configs = []

    max_order_p = 5
    max_order_i = 1
    max_order_q = 2

    p_orders = range(1, max_order_p + 1)
    i_orders = range(1, max_order_i + 1)
    q_orders = range(1, max_order_q + 1)

    for p, i, q in product(p_orders, i_orders, q_orders):
        param_configs.append({'order': (p, i, q)})
    
    results = gridsearch_arima(global_deviations, n_test=12, param_configs=param_configs)
    # print result with minimum error
    print(min(results, key=lambda d: d['error']))


if __name__ == "__main__":


    