SHELL = /bin/sh

.SUFFIXES:
.SUFFIXES: .py .csv .pkl 

fetch-data:
	python src/fetch_data.py "data/NASA_GISS_LOTI_long_format.csv"

models/global_deviations_sarima.pkl: data/NASA_GISS_LOTI_long_format.csv models/param_grid_global.json
	python src/gridsearch.py  "data/NASA_GISS_LOTI_long_format.csv" "global" "models/param_grid_global.json" "models/global_deviations_sarima.pkl"

models/northern_deviations_sarima.pkl: data/NASA_GISS_LOTI_long_format.csv models/param_grid_northern.json
	python src/gridsearch.py  "data/NASA_GISS_LOTI_long_format.csv" "northern" "models/param_grid_northern.json" "models/northern_deviations_sarima.pkl"

create-forecast: data/NASA_GISS_LOTI_long_format.csv models/global_deviations_sarima.pkl models/northern_deviations_sarima.pkl
	python src/forecast.py "data/NASA_GISS_LOTI_long_format.csv" "global" "models/global_deviations_sarima.pkl" "2019-01-01" "2020-02-01" "models/global_deviations_forecast.csv" 
	python src/forecast.py "data/NASA_GISS_LOTI_long_format.csv" "northern" "models/northern_deviations_sarima.pkl" "2019-01-01" "2020-02-01" "models/northern_deviations_forecast.csv"

upload-data: data/NASA_GISS_LOTI_long_format.csv models/global_deviations_forecast.csv models/northern_deviations_forecast.csv
	python src/upload_data.py "data/NASA_GISS_LOTI_long_format.csv" "tempdev-data" "data"
	python src/upload_data.py "models/global_deviations_forecast.csv" "tempdev-data" "models" 
	python src/upload_data.py "models/northern_deviations_forecast.csv" "tempdev-data" "models"
