SHELL = /bin/sh

.SUFFIXES:
.SUFFIXES: .py .csv .pkl .json

# file paths
# file where data should be saved
data_path = data/NASA_GISS_LOTI_long_format.csv 

# grid search parameters and model dumps
global_temp_params = models/param_grid_global.json
global_temp_model = models/global_deviations_sarima.pkl
northern_temp_params = models/param_grid_northern.json
northern_temp_model = models/northern_deviations_sarima.pkl

# forecast
forecast_start = "2019-01-01"
forecast_end = "2020-02-01"
global_temp_forecast = models/global_deviations_forecast.csv
northern_temp_forecast = models/northern_deviations_forecast.csv

# S3 bucket
bucket_name = tempdev-data


fetch-data:
	python src/fetch_data.py $(data_path)

$(global_temp_model): $(data_path) $(global_temp_params)
	python src/gridsearch.py $(data_path) "global" $(global_temp_params) $(global_temp_model)

$(northern_temp_model): $(data_path) $(northern_temp_params)
	python src/gridsearch.py $(data_path) "northern" $(northern_temp_params) $(northern_temp_model)

$(global_temp_forecast): $(data_path) $(global_temp_model)
	python src/forecast.py $(data_path) "global" $(global_temp_model) $(forecast_start) $(forecast_end) $(global_temp_forecast)

$(northern_temp_forecast): $(data_path) $(northern_temp_model)
	python src/forecast.py $(data_path) "northern" $(northern_temp_model) $(forecast_start) $(forecast_end) $(northern_temp_forecast)

upload-data: $(data_path) $(global_temp_forecast) $(northern_temp_forecast)
	python src/upload_data.py $(data_path) $(bucket_name) "data"
	python src/upload_data.py $(global_temp_forecast) $(bucket_name) "models" 
	python src/upload_data.py $(northern_temp_forecast) $(bucket_name) "models"
