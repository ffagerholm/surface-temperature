import pickle
import pandas as pd
import statsmodels.api as sm


def train_model(data_path, key, model_path):
    print("Reading model")
    with open(model_path, 'rb') as infile:
        model_fit = pickle.load(infile)
    print("Done.")

    monthly_deviations = pd.read_csv(data_path, 
                                     index_col='Date', 
                                     parse_dates=['Date'])

    # take deviations from mean up 
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
    print("Generate predictions and save to file.")
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
    model_fit = train_model(data_path='../data/NASA_GISS_LOTI_long_format.csv', 
                            key='global', 
                            model_path='../models/global_deviations_sarima.pkl')
    create_forecast(model_fit, 
                    start='2019-02-01', end='2020-02-01', 
                    output_path='../models/global_deviations_forecast.csv', )


if __name__ == "__main__":
    main()