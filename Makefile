SHELL = /bin/sh

.SUFFIXES:
.SUFFIXES: .py .csv .pkl 

fetch-data: src/fetch_data.py
    python src/fetch_data.py "data/NASA_GISS_LOTI_long_format.csv"

