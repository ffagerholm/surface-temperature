"""
Run gridsearch with corss-validation over different configurations for a SARIMA model.
The best model is saved to a file.

To run 
    python src/gridsearch.py <data path> <column name> <model output path>

where 
    <data path>: Path to training data.
    <column name>: Column name for time series (either "global" or "northern").
    <model output path> Path to file where the best model should be saved.

Example:
    python src/gridsearch.py  'data/NASA_GISS_LOTI_long_format.csv' 'global' 'models/global_deviations_sarima.pkl'
"""
import sys
from itertools import product 
import pickle
import pandas as pd
import statsmodels.api as sm
from sklearn.base import BaseEstimator, RegressorMixin
from sklearn.model_selection import TimeSeriesSplit
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import mean_squared_error

from sm_wrapper import SARIMAXWrapper


def aic_scorer(estimator, X, y):
    """Get the AIC from a statsmodels model.
    Sklearn style scorer function.
    """
    estimator.fit(X)
    aic = estimator.results_.aic

    return aic


def create_model_order_configs(p_lim=(0, 1), i_lim=(0, 1), q_lim=(0, 1)):
    """Crete configurations of model orders.
    Create all configureations between the given limits.
    Args:
        p_lim (tuple): tuple containing the lower and upper limits 
            for the AR order
        i_lim (tuple): tuple containing the lower and upper limits 
            for the differencing order
        q_lim (tuple): tuple containing the lower and upper limits 
            for the MA order
    
    Returns (list(tuple)): list of model orders of the form (p, i, q)
        where p, i and q are integers
    """
    # create ranges of the orders
    p_orders = range(p_lim[0], p_lim[1] + 1)
    i_orders = range(i_lim[0], i_lim[1] + 1)
    q_orders = range(q_lim[0], q_lim[1] + 1)
    # take the cartesian product between the ranges 
    # to get all possible triples
    model_orders = list(product(p_orders, i_orders, q_orders))
    
    return model_orders


def run_gridsearch(data_path, key, model_output_path):
    print("Reading training data from file:", data_path)
    monthly_deviations = pd.read_csv(data_path, 
                                     index_col='Date', 
                                     parse_dates=['Date'])
    print("Done.")
    # take deviations from mean up to (and including) 2018-01
    train_data = monthly_deviations[key][:'2018-01']

    model_orders = create_model_order_configs((1, 11), (1, 1), (1, 1))
        
    param_grid = {
        'order': model_orders,
        'seasonal_order': [(1, 1, 1, 12),],
        'trend': ['ct',],
    }
    cv = TimeSeriesSplit(n_splits=3)
    model = SARIMAXWrapper(freq='MS')

    print("Running grid search")
    grid = GridSearchCV(model, 
                        param_grid=param_grid,
                        scoring='neg_mean_squared_error', 
                        cv=cv, 
                        n_jobs=1,
                        verbose=3)
    # run grid search
    grid.fit(train_data, train_data)       
    print("Done.")     

    print("Best model found through grid search:", grid.best_estimator_)
    # get the SARIMAXResultsWrapper from the model 
    # that fit the training data best.
    model_fit = grid.best_estimator_.results_

    print("Saving best model to file:", model_output_path)
    with open(model_output_path, 'wb') as outfile:
        pickle.dump(model_fit, outfile)
    print("Done.")


def main():
    if len(sys.argv) == 4:
        data_path = sys.argv[1]
        key = sys.argv[2]
        model_output_path = sys.argv[3]

        run_gridsearch(data_path, key, model_output_path)
    else:
        raise RuntimeError('Not enough commandline arguments.')    
    

if __name__ == "__main__":
    main()

    