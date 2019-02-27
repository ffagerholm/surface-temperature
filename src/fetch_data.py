"""
Fetch temperature deviations data from 
https://data.giss.nasa.gov/gistemp/

The data are monthly observations in tabular format of temperature anomalies, 
i.e. deviations from the corresponding 1951-1980 means. 
Combined Land-Surface Air and Sea-Surface Water Temperature Anomalies 
(Land-Ocean Temperature Index, LOTI)

Data are updated monthly.

The script is run by giving the path to where the data should be saved
    python src/fetch_data.py <data path>

Example:
    python src/fetch_data.py "data/NASA_GISS_LOTI_long_format.csv"
"""
import sys
import pandas as pd

# urls for fetching the csv
GLOBAL_MEANS_URL = "https://data.giss.nasa.gov/gistemp/tabledata_v3/GLB.Ts+dSST.csv"
NORTHERN_MEANS_URL = "https://data.giss.nasa.gov/gistemp/tabledata_v3/NH.Ts+dSST.csv"


def fetch_data(global_temp_url, northern_temp_url, data_path):
    # read data returned in the request to the url, 
    # skip first row as it contains the data set name
    print("Fetching data from URLs:", global_temp_url, northern_temp_url, sep='\n')
    data_sets = {
        # Global-mean monthly, seasonal, and annual means, 1880-present
        'global': pd.read_csv(global_temp_url, skiprows=[0]),
        # Northern Hemisphere-mean monthly, seasonal, and annual means, 1880-present
        'northern': pd.read_csv(northern_temp_url, skiprows=[0])
    }
    print("Done.")

    print("Transforming data to long format")
    # tranform the data sets to a suitable form for modeling
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
              'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    for key in data_sets:
        # unpivot the tabular data into a time series in long format
        data_sets[key] = data_sets[key].melt(id_vars=['Year'], var_name='Month', 
                                            value_vars=months, value_name=key)

        # convert the deviation values into numeric form
        # missing values seems to be represented with "***" these will be converted to NaNs
        # add a new column with the same name as `key`
        data_sets[key][key] = pd.to_numeric(data_sets[key][key], errors='coerce')
        # Combine the year and month, and convert to datetime
        data_sets[key]['Date'] = pd.to_datetime(data_sets[key]['Year'].astype(str) + ' ' + data_sets[key]['Month'])
        # set the date as index
        data_sets[key].set_index('Date', inplace=True)
        data_sets[key].sort_index(inplace=True)
    print("Done.")

    # combine data frames
    monthly_deviations = pd.concat([data_sets[key][key] for key in data_sets], axis=1)
    print("Saving data to file:", data_path)
    # save data to file
    monthly_deviations.to_csv(data_path)
    print("Done.")

def main():
    if len(sys.argv) == 2:
        data_path = sys.argv[1]
        fetch_data(GLOBAL_MEANS_URL, NORTHERN_MEANS_URL, data_path)
    else:
        raise RuntimeError('Not enough commandline arguments.')    
    
    


if __name__ == "__main__":
    main()