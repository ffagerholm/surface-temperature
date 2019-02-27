SHELL = /bin/sh

.SUFFIXES:
.SUFFIXES: .py .csv .pkl 

fetch-data:
	python src/fetch_data.py "data/NASA_GISS_LOTI_long_format.csv"

models/global_deviations_sarima.pkl: data/NASA_GISS_LOTI_long_format.csv 
	python src/gridsearch.py  'data/NASA_GISS_LOTI_long_format.csv' 'global' 'models/global_deviations_sarima.pkl'

models/northern_deviations_sarima.pkl: data/NASA_GISS_LOTI_long_format.csv 
	python src/gridsearch.py  'data/NASA_GISS_LOTI_long_format.csv' 'northern' 'models/northern_deviations_sarima.pkl'

create-forecast: data/NASA_GISS_LOTI_long_format.csv models/global_deviations_sarima.pkl models/northern_deviations_sarima.pkl
	python src/forecast.py "data/NASA_GISS_LOTI_long_format.csv" "global" "models/global_deviations_sarima.pkl" "2019-01-01" "2020-02-01" "models/global_deviations_forecast.csv" 
	python src/forecast.py "data/NASA_GISS_LOTI_long_format.csv" "northern" "models/northern_deviations_sarima.pkl" "2019-01-01" "2020-02-01" "models/northern_deviations_forecast.csv"
