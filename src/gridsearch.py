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
    python src/gridsearch.py  'data/NASA_GISS_LOTI_long_format.csv' 'global' 'models/param_grid_global.json' 'models/global_deviations_sarima.pkl'
"""
import sys
from itertools import product 
import pickle
import json
import pandas as pd
import statsmodels.api as sm
from sklearn.base import BaseEstimator, RegressorMixin
from sklearn.model_selection import TimeSeriesSplit
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import mean_squared_error

from sm_wrapper import SARIMAXWrapper


def run_gridsearch(data_path, key, param_grid_path, model_output_path):
    print("Reading training data from file:", data_path)
    monthly_deviations = pd.read_csv(data_path, 
                                     index_col='Date', 
                                     parse_dates=['Date'])
    print("Done.")
    # take deviations from mean temperatures
    train_data = monthly_deviations[key]
    
    with open(param_grid_path, 'rb') as infile:
        param_grid = json.loads(infile.read())

    cv = TimeSeriesSplit(n_splits=3)
    model = SARIMAXWrapper()

    print("Running grid search")
    grid = GridSearchCV(model, 
                        param_grid=param_grid,
                        scoring='neg_mean_squared_error', 
                        cv=cv, 
                        n_jobs=1,
                        verbose=2)
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
    if len(sys.argv) == 5:
        data_path = sys.argv[1]
        key = sys.argv[2]
        param_grid_path = sys.argv[3]
        model_output_path = sys.argv[4]

        run_gridsearch(data_path, key, param_grid_path, model_output_path)
    else:
        raise RuntimeError('Not enough commandline arguments.')    
    

if __name__ == "__main__":
    main()

    