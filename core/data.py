import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import random

def generate_power_data(start_year: int, num_of_years: int) -> pd.DataFrame:
    '''Generates random power data for Ghana for a given number of years starting from a given year.'''
    starting_year = datetime(start_year, 1, 1)
    end_date = starting_year + timedelta(days=num_of_years * 365)
    date_range = pd.date_range(start=str(start_year), end=str(end_date), freq='D')
    regions = [
    "Ashanti Region",
    "Brong-Ahafo Region",
    "Central Region",
    "Eastern Region",
    "Greater Accra Region",
    "Northern Region",
    "Upper East Region",
    "Upper West Region",
    "Volta Region",
    "Western Region",
    "Ahafo Region",
    "Bono East Region",
    "North East Region",
    "Oti Region",
    "Savannah Region",
    "Western North Region"
]
    districts = ['District one', 'District Two', 'District Three', 'District Four', 'District Five']
    towns = ['Town One', 'Town Two', 'Town Three', 'Town Four', 'Town Five']
    grids = ['Grid One', 'Grid Two', 'Grid Three', 'Grid Four', 'Grid Five']
    #Assuming the ratio of non-holidays to holidays is 352:13 for Ghana
    non_holidays = ("A " * 352).strip(" ").split(" ")
    holidays = ("B " * 13).strip(" ").split(" ")
    combined = non_holidays + holidays
    random.shuffle(combined)
    #Assuming the ratio of non-power out to power out 300:65 for Ghana
    no_power_out = ("A " * 300).strip(" ").split(" ")
    power_out = ("B " * 65).strip(" ").split(" ")
    combined_power = no_power_out + power_out
    random.shuffle(combined_power)
    
    
    data = {
        'Date': date_range,
        'Region': np.random.choice(regions, size=len(date_range)),
        'District': np.random.choice(districts, size=len(date_range)),
        'Town': np.random.choice(towns, size=len(date_range)),
        'Grid': np.random.choice(grids, size=len(date_range)),
        'Power_Consumption_MWh': np.random.randint(500, 2000, size=len(date_range)),
        'Power_Generation_MWh': np.random.randint(400, 1800, size=len(date_range)),
        'Power_Outage': np.random.choice(combined_power, size=len(date_range)),
    }

    df_power = pd.DataFrame(data)
    print('Dataframe Created Successfully!')
    # save dataframe into googlesheet
    
    # save to csv
    df_power.to_csv('power_data.csv', index=False)
    return df_power


generate_power_data(2015, 5)