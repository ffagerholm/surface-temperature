# Reaktor Machine learning task

Implementation of the [task](https://www.reaktor.com/ennakkotehtava-koneoppiminen/) for the position as a machine learning intern at Reaktor.

We have created a web application that visualizes the changes in temperatures globally versus in the northern hemisphere.
The resulting web application can be viewed [here](http://tempdev-dashboard.herokuapp.com/). The app can also be viewed 
on mobile devices.  

The app contains a plot of the deviations in mean temperatures compared to a reference period during 1951 to 1980. The plot is based on data from [NASA](https://data.giss.nasa.gov/gistemp/) which contains the temperature deviations from
the period 1880-01-01 to 2019-02-01. The plot also shows a one year forecast that has been generated using a SARIMA model.

This repository contains the code for the web app, as well as code for fetching and cleaning data, model selection and forecast generation.

## Getting Started

### Prerequisites

Before running the code the following prerequisites should be installed.  
All code is written in `Python 3.6.8`.  
To install the requred packages, run  
```
pip install -r requirements.txt
```

### Running 

The jupyter notebooks in the directory `notebook/` are used for exploring the data and building and evaluating models.
After installing [Jupyter](https://jupyter.org/) these can be run with the command  
```
jupyter notebook notebooks/
```

The scripts for fetching the data, model selection and forecasting can be run locally. They are found in the directory `scr/`. 
They should be run as a pipeline in the order
1. fetch_data.py
2. gridsearch.py
3. forecast.py  

This can be done by running the command  
```
make models/global_deviations_forecast.csv
make models/northern_deviations_forecast.csv
```
All the steps of the pipeline will be run in the correct order.  

And to upload the files to Amazon S3, run  
```
make upload-data
```
> Note that for uploading (and fetching) data the access and secret keys should be stored in a file named `.env` in the root directory.  

Example of the `.env` file:
```
AWS_ACCESS_KEY_ID=<access key>
AWS_SECRET_ACCESS_KEY=<secret key>
```

The web application is deployed on [Heroku](https://www.heroku.com) and fetches data stored on [Amazon S3](https://aws.amazon.com/s3/).  

The data are updated on NASAs website around the middle of every month [source](https://data.giss.nasa.gov/gistemp/). Thus, the data used by the web app should also be updated with the same frequency. This can be done by scheduling the pipeline to run every month (using for example `cron`), which would update the data and forecasts.  

## Project structure

    ├── README.md          <- The top-level README for this project.
    ├── LICENCE
    ├── Procfile           <- For Heroku deployment.
    ├── Makefile           <- Makefile for running the data pipeline
    ├── app                <- Code for web application.
    │   ├── static
    |   |     ├── css      <- Styling.
    |   |     ├── js       <- Frontend code.
    │   ├── templates      <- Jinja templates.
    │   └── __init__.py    <- Application code.
    |
    ├── data               <- Data used in this project
    │
    ├── models             <- Trained and serialized models and model predictions
    │
    ├── notebooks          <- Jupyter notebooks.
    │
    ├── requirements.txt   <- The requirements file for reproducing the analysis environment, 
    │                         generated with `pip freeze > requirements.txt`
    |
    ├── src                <- Script used in this project.
    │   ├── fetch_data.py  <- Scripts for downloading and cleaning data-
    │   ├── gridsearch.py  <- Model selection.
    │   ├── forecast.py    <- Generating forecasts.
    │   └── sm_wrapper.py  <- Scikit learn wrapper for statsmodels models.
    |
    └─────── tests



## Built With

* [Pandas](https://pandas.pydata.org/) - Data cleaning and manipulation
* [Scikit-learn](https://scikit-learn.org/) - Cross-validation and model selection
* [StatsModels](http://www.statsmodels.org/dev/index.html) - Time-series models
* [Plotly](https://plot.ly/) - Plotting and web frontend
* [Flask](http://flask.pocoo.org/) - Web backend


## Authors

* **Fredrik Fagerholm** - [ffagerholm](https://github.com/ffagerholm)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details
