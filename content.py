api_code='''# Import necessary libraries
import os
import requests
import pandas as pd

# ----------------------------------------------------------------------------------------------------------
# NYC Open Data API
# This script defines functions to retrieve and process health inspection data from the NYC Open Data API.
# __________________________________________________________________________________________________________

# Function to check if a CSV file exists for the specified year range and load it if it does.
def check_and_load_csv(start_year, end_year):
    # Define the filename based on the year range
    filename = f'nyc_health_inspections_{start_year}_to_{end_year}.csv' if start_year != end_year else f'nyc_health_inspections_{start_year}.csv'
    
    # Check if the file exists
    if os.path.isfile(filename):
        print(f"CSV file for {start_year} to {end_year} already exists. Loading data from the CSV.")
        return pd.read_csv(filename)
    
    # If the file doesn't exist, return None
    return None

# Function to make an API request to NYC Open Data and retrieve inspection data for a specified year range.
def make_api_request(start_year, end_year, app_token, offset, page_size):
    # Define the base URL for the API
    base_url = 'https://data.cityofnewyork.us/resource/43nn-pn8j.json'
    
    # Construct the API request URL with filters, app token, offset, and page size
    url = f'{base_url}?$where=inspection_date between "{start_year}-01-01T00:00:00.000" and "{end_year}-12-31T23:59:59.999"&$$app_token={app_token}&$offset={offset}&$limit={page_size}'
    
    # Make an HTTP GET request to the API
    response = requests.get(url)
    
    # Check if the request was successful (status code 200)
    if response.status_code != 200:
        raise Exception(f"Failed to retrieve data. Status code: {response.status_code}")
    
    # Return the response data in JSON format
    return response.json()

# Function to process data by making API requests and accumulating the results.
def process_data(start_year, end_year, app_token, max_observations=None):
    offset = 0
    page_size = 1000
    all_data = []
    
    # Continue making API requests until reaching the specified number of observations or the end of data.
    while max_observations is None or len(all_data) < max_observations:
        remaining_observations = max_observations - len(all_data) if max_observations is not None else page_size
        actual_page_size = min(page_size, remaining_observations)
        data = make_api_request(start_year, end_year, app_token, offset, actual_page_size)
        
        # Break the loop if no more data is available
        if not data:
            break
        
        # Accumulate the retrieved data
        all_data.extend(data)
        offset += actual_page_size
        
        # Break the loop if the specified number of observations is reached
        if max_observations is not None and len(all_data) >= max_observations:
            break

    # Convert the accumulated data to a DataFrame
    return pd.DataFrame(all_data)

# Function to get health inspection data, either from a CSV file or by making API requests.
def get_health_inspection_data(start_year, end_year, app_token, max_observations=None):
    # Check if the end year is greater than or equal to the start year
    if end_year < start_year:
        raise ValueError("End year must be greater than or equal to start year")

    # Attempt to load data from a CSV file
    df = check_and_load_csv(start_year, end_year)
    
    # If data is found in the CSV, return it
    if df is not None:
        return df

    # If data is not in the CSV, retrieve it using API requests
    df = process_data(start_year, end_year, app_token, max_observations)
    
    # Save the retrieved data to a CSV file
    csv_filename = f'nyc_health_inspections_{start_year}_to_{end_year}.csv' if start_year != end_year else f'nyc_health_inspections_{start_year}.csv'
    df.to_csv(csv_filename, index=False)
    print(f"Health inspection data from {start_year} to {end_year} retrieved and saved to {csv_filename}.")
    
    # Return the retrieved data as a DataFrame
    return df'''

api_call='''
# Import necessary libraries
import pandas as pd
import numpy as np
import env  # Holds API token
import acquire as a  # NYC Open Data API module

# Define function variables
app_token = env.app_token  # Get the application token
start_year = '2000'
end_year = '2023'

# Retrieve health inspection data
inspections_df = a.get_health_inspection_data(start_year, end_year, app_token, max_observations=None)

# Display the first 5 rows of the data
inspections_df.head(5)
'''

nyc_acquired_df='''
| **camis**     | **dba**             | **boro**   | **building** | **street**         | **zipcode** | **phone**  | **cuisine_description** | **inspection_date**         | **action**                                    | **critical_flag** | **score** | **record_date**          | **inspection_type**                          | **latitude**     | **longitude**      | **community_board** | **council_district** | **census_tract** | **bin** | **bbl**      | **nta** | **violation_code** | **violation_description** | **grade** | **grade_date** |
|:------------:|:-------------------:|:----------:|:------------:|:-------------------:|:-----------:|:----------:|:---------------------:|:-----------------------------:|:----------------------------------------------:|:-----------------:|:---------:|:------------------------:|:---------------------------------------------:|:----------------:|:------------------:|:-----------------:|:-------------------:|:---------------:|:-------:|:------------:|:-------:|:-----------------:|:------------------------:|:---------:|:--------------:|
|   50067297   | GERBASI RESTAURANT  |   Bronx    |     2389     |   ARTHUR AVENUE    |    10458    | 7182205735 |        Italian         |    2021-09-12T00:00:00.000   | No violations were recorded at the time of this inspection. | Not Applicable  |     0     | 2023-12-01T06:00:08.000 | Inter-Agency Task Force / Initial Inspection  | 40.855290482438 | -73.887796721867 |       206         |         15          |      039100     |  2011897  |  2030650046  |   BX06  |       NaN        |   NaN   |        NaN        |         NaN          |    NaN    |       NaN      |
|   50034232   |  RELISH CATERERS    |   Bronx    |     2501     |      3 AVENUE      |    10451    | 2122281672 |       American         |    2021-09-25T00:00:00.000   | No violations were recorded at the time of this inspection. | Not Applicable  |     0     | 2023-12-01T06:00:08.000 | Inter-Agency Task Force / Initial Inspection  | 40.810202180315 | -73.928401164709 |       201         |         08          |      005100     |  2000795  |  2023200047  |   BX39  |       NaN        |   NaN   |        NaN        |         NaN          |    NaN    |       NaN      |
|   50064240   |    DAXI SICHUAN     |   Queens   |    136-20    | ROOSEVELT AVENUE   |    11354    | 9175631983 |        Chinese        |    2022-09-21T00:00:00.000   | Violations were cited in the following area(s). |    Not Critical   |    13     | 2023-12-01T06:00:08.000 | Cycle Inspection / Initial Inspection         | 40.759777908235 | -73.829235428489 |       407         |         20          |      085300     |  4113546  |  4050190005  |   QN22  |       09B        |  Thawing procedure improper.  |     A     |  2022-09-21T00:00:00.000  |
|   50105603   | LE PAIN QUOTIDIEN   | Manhattan  |      81      |  WEST BROADWAY     |    10007    | 6468639168 |        French         |    2022-11-25T00:00:00.000   | No violations were recorded at the time of this inspection. | Not Applicable  |   NaN     | 2023-12-01T06:00:09.000 | Administrative Miscellaneous / Re-inspection | 40.715082569302 | -74.009566501861 |       101         |         01          |      002100     |  1001480  |  1001367503  |   MN24  |       NaN        |   NaN   |        NaN        |         NaN          |    NaN    |       NaN      |
|   50069583   |       PHO BEST      |   Queens   |     4235     |      MAIN ST       |    11355    | 9173618878 | Southeast Asian  |    2022-05-09T00:00:00.000   | Violations were cited in the following area(s). |     Critical      |    30     | 2023-12-01T06:00:08.000 | Cycle Inspection / Initial Inspection         | 40.754418104812 | -73.827881250044 |       407         |         20          |      085300     |  4573539  |  4051357502  |   QN22  |       02B        | Hot food item not held at or above 140º F. |   NaN    |       NaN      |

'''

prep_text='''
For the NYC Health Inspection dataset, we undertook a thorough and thoughtful preparation process to ensure the data's integrity and relevance for our analysis. This process involved a deep dive into the dataset to understand and address the presence of null values, rather than simply removing them. We explored innovative methods to infer missing data from other related fields, particularly focusing on geographical information. Additionally, we closely analyzed inspection types to filter out irrelevant data and standardized key columns like phone numbers and dates for consistency. 
'''

