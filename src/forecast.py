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


def create_forecast(model_path, start, end, output_path, alpha=0.05):
    print("Reading model from file:", model_path)
    with open(model_path, 'rb') as infile:
        model_fit = pickle.load(infile)
    print("Done.")

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
    # check the the user provided enough cmd line arguments
    if len(sys.argv) == 5:
        model_path = sys.argv[1]
        start = sys.argv[2]
        end = sys.argv[3]
        output_path = sys.argv[4]

        create_forecast(model_path, 
                        start=start, end=end, 
                        output_path=output_path)
    else:
        raise RuntimeError('Not enough command line arguments.')


if __name__ == "__main__":
    main()