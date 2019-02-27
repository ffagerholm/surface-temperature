"""
Create a forecast using the the model found by gridsearch.
Specify the path to th model, data, and the start and end of the forecast period.
Example:
    python src/forecast.py "data/NASA_GISS_LOTI_long_format.csv" "global" "models/global_deviations_sarima.pkl" \
                           "2019-01-01" "2020-02-01" "models/global_deviations_forecast.csv"
"""
import sys
import pickle
import pandas as pd
import statsmodels.api as sm


def train_model(data_path, key, model_path):
    print("Reading model parameters from file:", model_path)
    with open(model_path, 'rb') as infile:
        model_fit = pickle.load(infile)
    print("Done.")

    print("Reading training data from file:", data_path)
    monthly_deviations = pd.read_csv(data_path, 
                                     index_col='Date', 
                                     parse_dates=['Date'])
    print("Done.")

    # take time-series from the column `key`
    data = monthly_deviations[key]

    print("Initialize and fit model.")
    model = sm.tsa.SARIMAX(data,
                           order=model_fit.model.order, 
                           seasonal_order=model_fit.model.seasonal_order,
                           freq='MS')
    model_fit = model.fit(disp=0)
    print("Done.")

    return model_fit


def create_forecast(model_fit, start, end, output_path, alpha=0.05):
    print("Generatng predictions and saving to file:", output_path)
    pred_res = model_fit.get_prediction(start=start, end=end, 
                                        full_results=True, alpha=alpha)
    # mean value
    pred_means = pd.DataFrame(pred_res.predicted_mean, columns=['forecast'])
    # (1 - alpha) confidence interval
    pred_cis = pred_res.conf_int(alpha=alpha)
    # combine prediction and confidence intervals 
    # into a dataframe 
    forecast = pd.concat([pred_means, pred_cis], axis=1)
    # save forecasted values
    forecast.to_csv(output_path)
    print("Done.")


def main():
    if len(sys.argv) == 7:
        data_path = sys.argv[1]
        key = sys.argv[2]
        model_path = sys.argv[3]
        start = sys.argv[4]
        end = sys.argv[5]
        output_path = sys.argv[6]

        model_fit = train_model(data_path=data_path, 
                                key=key, 
                                model_path=model_path)
        create_forecast(model_fit, 
                        start=start, end=end, 
                        output_path=output_path, )
    else:
        raise RuntimeError('Not enough commandline arguments.')


if __name__ == "__main__":
    main()