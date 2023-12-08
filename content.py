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
For the NYC Health Inspection dataset, we undertook a thorough and thoughtful preparation process to ensure the data's integrity and relevance for our analysis. This process involved a deep dive into the dataset to understand and address the presence of null values, rather than simply removing them. We explored innovative methods to infer missing data from other related fields, particularly focusing on zoning information. Additionally, we closely analyzed inspection types to filter out irrelevant data and standardized key columns like phone numbers and dates for consistency. 
'''

inspection_type = '''
['Administrative Miscellaneous / Compliance Inspection',
'Administrative Miscellaneous / Initial Inspection',
'Administrative Miscellaneous / Re-inspection',
'Administrative Miscellaneous / Reopening Inspection',
'Administrative Miscellaneous / Second Compliance Inspection',
'Calorie Posting / Compliance Inspection',
'Calorie Posting / Initial Inspection',
'Calorie Posting / Re-inspection',
'Cycle Inspection / Compliance Inspection',
'Cycle Inspection / Initial Inspection',
'Cycle Inspection / Re-inspection',
'Cycle Inspection / Reopening Inspection',
'Cycle Inspection / Second Compliance Inspection',
'Inter-Agency Task Force / Initial Inspection',
'Inter-Agency Task Force / Re-inspection',
'Pre-permit (Non-operational) / Compliance Inspection',
'Pre-permit (Non-operational) / Initial Inspection',
'Pre-permit (Non-operational) / Re-inspection',
'Pre-permit (Non-operational) / Second Compliance Inspection',
'Pre-permit (Operational) / Compliance Inspection',
'Pre-permit (Operational) / Initial Inspection',
'Pre-permit (Operational) / Re-inspection',
'Pre-permit (Operational) / Reopening Inspection',
'Pre-permit (Operational) / Second Compliance Inspection',
'Smoke-Free Air Act / Compliance Inspection',
'Smoke-Free Air Act / Initial Inspection',
'Smoke-Free Air Act / Limited Inspection',
'Smoke-Free Air Act / Re-inspection',
'Trans Fat / Compliance Inspection',
'Trans Fat / Initial Inspection',
'Trans Fat / Re-inspection']
'''


violation_description = '''
violation_description
“Choking first aid” poster not posted. “Alcohol and pregnancy” warning sign not posted. Resuscitation equipment: exhaled air resuscitation masks (adult & pediatric), latex gloves, sign not posted.                                                                                                                                                 763
Food allergy information poster not conspicuously posted where food is being prepared or processed by food workers.                                                                                                                                                                                                                                  699
Current letter grade or Grade Pending card not posted                                                                                                                                                                                                                                                                                                600
“Choking first aid” poster not posted. “Alcohol and Pregnancy” warning sign not posted. Resuscitation equipment: exhaled air resuscitation masks (adult & pediatric), latex gloves, sign not posted.                                                                                                                                                 585
Failure to post or conspicuously post healthy eating information                                                                                                                                                                                                                                                                                     438
Current letter grade sign not posted.                                                                                                                                                                                                                                                                                                                426
Providing single-use, non-compostable plastic straws to customers without customer request (including providing such straws at a self-serve station)                                                                                                                                                                                                 336
Nuisance created or allowed to exist.  Facility not free from unsafe, hazardous, offensive or annoying conditions.                                                                                                                                                                                                                                   218
Nuisance created or allowed to exist. Facility not free from unsafe, hazardous, offensive or annoying condition.                                                                                                                                                                                                                                     181
Lighting fixture located over, by or within food storage, preparation, service or display facility, and facility where utensils and equipment are cleaned and stored, which may shatter due to extreme heat, temperature changes or accidental contact; not fitted with shatterproof bulb or shielded and encased, with end caps or other device.    160
Failure to maintain a sufficient supply of single-use, non-compostable plastic straws.                                                                                                                                                                                                                                                               159
MISBRANDED AND LABELING                                                                                                                                                                                                                                                                                                                              146
Failure to display required signage about plastic straw availability.                                                                                                                                                                                                                                                                                133
Bulb not shielded or shatterproof, in areas where there is extreme heat, temperature changes, or where accidental contact may occur.                                                                                                                                                                                                                 126
Current letter grade or "Grade Pending" card not posted.                                                                                                                                                                                                                                                                                             104
Food Protection Certificate not available for inspection                                                                                                                                                                                                                                                                                             101
Failure to display required signage about plastic straw availability                                                                                                                                                                                                                                                                                  82
Manufacture of frozen dessert not authorized on Food Service Establishment permit. Milk or milk product undated, improperly dated or expired.                                                                                                                                                                                                         49
Equipment used for ROP not approved by the Department                                                                                                                                                                                                                                                                                                 45
Permit not conspicuously displayed.                                                                                                                                                                                                                                                                                                                   44
Sale or use of certain expanded polystyrene items restricted                                                                                                                                                                                                                                                                                          38
Providing single-use plastic stirrers or single-use plastic splash sticks.                                                                                                                                                                                                                                                                            38
ROP processing equipment not approved by DOHMH.                                                                                                                                                                                                                                                                                                       36
Current letter grade or "Grade Pending" card not conspicuously posted or visible to passersby                                                                                                                                                                                                                                                         28
Expanded Polystyrene (EPS) single service article not designated as a recyclable material.                                                                                                                                                                                                                                                            24
Current valid permit, registration or other authorization to operate a Food Service Establishment (FSE) or Non-retail Food Processing Establishment (NRFP) not available.                                                                                                                                                                             20
Providing compostable plastic straws to be used outside of the food establishment’s premises; failure to appropriately dispose of compostable plastic straws; failure to maintain required bins for disposal of compostable plastic straws.                                                                                                           15
Letter grade or Grade Pending card not conspicuously posted and visible to passersby.                                                                                                                                                                                                                                                                 13
Order or notice posted or required to be posted by the Department mutilated, obstructed or removed.                                                                                                                                                                                                                                                   11
Failure to comply with an Order of the Board of Health, Commissioner, or Department.                                                                                                                                                                                                                                                                   8
Failure to comply with an order of the Board of Health, Commissioner or Department.                                                                                                                                                                                                                                                                    8
Document issued by the Board of Health, Commissioner or Department reproduced or altered. False, untrue or misleading statement or document made to, submitted or filed with the Department                                                                                                                                                            8
Notice of the Department of Board of Health mutilated, obstructed, or removed.                                                                                                                                                                                                                                                                         5
Document issued by the Board of Health, Commissioner or Department unlawfully reproduced or altered.                                                                                                                                                                                                                                                   5
Letter grade or Grade Pending card removed, destroyed, modified, obscured, or otherwise tampered with                                                                                                                                                                                                                                                  3
Food allergy information poster not posted in language understood by all food workers.                                                                                                                                                                                                                                                                 2
Current valid permit, registration or other authorization to operate a Temporary Food Service Establishment (TFSE) not available.                                                                                                                                                                                                                      2
Failure to post signage in organics collection area.                                                                                                                                                                                                                                                                                                   1
Organics containers not provided                                                                                                                                                                                                                                                                                                                       1
Document issued by the Board of Health, Commissioner or Department reproduced or altered.  False, untrue or misleading statement or document made to, submitted or filed with the Department                                                                                                                                                           1
Food allergy poster does not contain text provided or approved by Department.                                                                                                                                                                                                                                                                          1
Failure to provide a single-use, non-compostable plastic straw upon request.                                                                                                                                                                                                                                                                           1
Toilet facility used by women does not have at least one covered garbage receptacle.                                                                                                                                                                                                                                                                   1
'''