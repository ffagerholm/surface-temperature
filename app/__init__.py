import json
import plotly
import pandas as pd
from flask import Flask, render_template
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

app = Flask(__name__)

monthly_deviations = pd.read_csv("s3://tempdev-data/data/NASA_GISS_LOTI_long_format.csv",
                                 index_col='Date', 
                                 parse_dates=['Date'])
global_forecast = pd.read_csv("s3://tempdev-data/models/global_deviations_forecast.csv", 
                              index_col=0)
northern_forecast = pd.read_csv("s3://tempdev-data/models/northern_deviations_forecast.csv", 
                                index_col=0)


@app.route('/')
def index():
    graphs = dict(
        global_data=dict(
            x=monthly_deviations['global'].index,
            y=monthly_deviations['global'],
            name='Golbal', 
        ),
        global_forecast=dict(
            index=global_forecast['forecast'].index,
            mean=global_forecast['forecast'],
            ci_lower=global_forecast['lower global'],
            ci_upper=global_forecast['upper global'],
            name='Golbal forecast', 
        ),
        northern_data=dict(
            x=monthly_deviations['northern'].index,
            y=monthly_deviations['northern'],
            name='Northern hemisphere',
        ),
        northern_forecast=dict(
            index=northern_forecast['forecast'].index,
            mean=northern_forecast['forecast'],
            ci_lower=northern_forecast['lower northern'],
            ci_upper=northern_forecast['upper northern'],
            name='Northern hemisphere forecast', 
        ),

    )

    # Convert the figures to JSON
    # PlotlyJSONEncoder converts objects to their JSON equivalents
    graphJSON = json.dumps(graphs, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('index.html',
                           graphJSON=graphJSON)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
