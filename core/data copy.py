import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import random

import gspread
from google.oauth2 import service_account
from google.oauth2.service_account import Credentials

# Authenticate with Google Sheets


def authenticate_google_sheets():
    scopes = [
        'https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/drive'
    ]

    credentials = {
        "type": "service_account",
        "project_id": "energia-ai",
        "private_key_id": "6452cea594a81b02141ad98612a13fbf22596229",
        "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQDbm25bf21cUVzy\nJVgkBg50LUv3iyshOJjO01qsMCI8RY137WIbvdTE/qS/KS9cJZxNAOXTi6VT6X5e\nzf04jUBAGYDrZxiDnB13QUX0P4CDgbIPPpPbze806zKFJwpn6FGrNK2Um1S/dgpa\nyeabNni8mIF0P3shHtVWOYEil8HLvuFeGFLuVuTX8k7PiedffDRc3GqkC2dxT9UW\nU1CsCCnW1V2U/XpB8a072tMJPw5+1A+eOxj7Nr9puWXMUNxVR/+N6He33Ksj6Utx\nwNs/2aBxOLEoU4p9jwKll9a43X/Toxs1u9QBzVv+iq7cvvvy7PWJ/Iph9VZVirhr\nX7r7vXn3AgMBAAECggEANlTQCscN8WcXzbi7g74T2V5TixzdQMzV0WWs6yjFb4/t\nnhwWx7JBb7NoYvr3gp6zesGcGqhT8Ny1rRLdcR5RJQqqQJMzF2yKRbTab8E+NErk\nGK1su1bJtZfy2cp84pQxkF/qCfgcEXpMuYV2DjR9znsUnAQQnHMaaMi1UC+nfJZ5\nW5Be3ZGVIs3oqXP5Os9Kdw3i5D1OYg3C9VIL4A3OoyvmUmg6l/2jsXlNFfYdlNvG\nmi8kgYiX0RPP+zWH3X5uPwDtAngvH+PGnMsn1Z4sAtqfsWmx7Qn/wzFJiSFe1UK6\n+mfvTT0ZYh4yfaJDSti92hA7N5taVfmRMU2sZAKr8QKBgQD/L1eT+2mQDOxoYvbh\nH4gvOP0DHpBa3wYThUbyP2mUd1ZXc60585dOG9Qe2oYIgrIAxmEPod21SVRYkx3+\n0KyKwmafW9qMjcw6LpkzRng5QrbYJelboI80M47guDpNS51toZlmrB35YiKB3KBr\nMLNQx1/020gnSX0E5NIHbna3pQKBgQDcTv974QP2Feii05IQ+U5Hy4tgim9rMCyP\n+PxvURa5vCsJD9+5ZyNGCO1epnpRQClUUIumX72f54+R7ZwIkuAsXWCgEOXVEov9\n5W+krYfm7bs/SfKj+SLYT3j0kyzQOFvRbtOtUvaNKI4fXJEdUyqBwmu+rJ+zdnjD\nPM5YfKZYawKBgDZRX3TyaQ/ukEvP9PkKezSCDukhEl0lZ+ez0Nwzv0eI92n6B390\naFqJ9ebzYOBi4XzkvThUnhq+lyObfSEGThPjOXDmXmjYrgYccSPG9kRJ/R2ZREjq\nrlDQQLN4w4A8fjAd28dND7xLtUirK8JlRWYGalh2bK9gJyppgoNucfq5AoGBAM5w\nTCDlylN3ViX1wQKcyoimJ/WP4zX6z1cdxlX9EyF6PI1iTY8rITeIN/2gXC/0woWa\ncDG3tzW2w6bHk5XJI70OxvNWwjb2CS4iJ4qVfSqcjACTJ4YVd1xgpAPyQWTf2tIW\nWs4oVpYRcZPbprNm8gbjixkCIygElMbGHMl4DFv/AoGBAJf/uV+MveMqW0JCeLZq\ndAbhqZVPL+RmgZVjUYm9NhFYE98FW/qXO0iizIRDSyUMKc92MNtAmCLY353LZfMu\n+oYvZQSaZnPk6oBtAaq3Vpwh6cjBkfPREPM50IkAB++s96U3puZ0eTn8GougJoce\nzk8WpKPxnzz/D0oricWMJ5pW\n-----END PRIVATE KEY-----\n",
        "client_email": "energia-data@energia-ai.iam.gserviceaccount.com",
        "client_id": "106231224975832618998",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/energia-data%40energia-ai.iam.gserviceaccount.com",
        "universe_domain": "googleapis.com"
    }

    gc = gspread.service_account_from_dict(credentials)
    return gc


def create_or_update_worksheet(gc, sheet_name, data):
    # if worksheet doesn't exist, create a new one
    try:
        worksheet = gc.open(sheet_name).sheet1
        print('Worksheet Found!')
    except gspread.exceptions.SpreadsheetNotFound:
        worksheet = gc.create(sheet_name).sheet1
        print('Worksheet Created!')

    # Convert the DataFrame to a list of lists (2D array) for easy uploading to Google Sheets
    data_to_upload = [data.columns.tolist()] + data.values.tolist()

    # Clear existing data and update the worksheet with the new data
    # worksheet.clear()
    worksheet.update(values=data_to_upload, range_name="A1")
    print('Worksheet Updated Successfully!')


def generate_power_data(start_year: int, num_of_years: int) -> pd.DataFrame:
    '''Generates random power data for Ghana for a given number of years starting from a given year.'''

    starting_year = datetime(start_year, 1, 1)
    end_date = starting_year + timedelta(days=num_of_years * 365)
    date_range = pd.date_range(
        start=str(start_year), end=str(end_date), freq='D')
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
    districts = ['District one', 'District Two',
                 'District Three', 'District Four', 'District Five']
    towns = ['Town One', 'Town Two', 'Town Three', 'Town Four', 'Town Five']
    grids = ['Grid One', 'Grid Two', 'Grid Three', 'Grid Four', 'Grid Five']
    # Assuming the ratio of non-holidays to holidays is 352:13 for Ghana
    non_holidays = ("A " * 352).strip(" ").split(" ")
    holidays = ("B " * 13).strip(" ").split(" ")
    combined = non_holidays + holidays
    random.shuffle(combined)
    # Assuming the ratio of non-power out to power out 300:65 for Ghana
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
    
    # Convert the 'Date' column to string format
    data['Date'] = data['Date'].strftime('%Y-%m-%d')

    df_power = pd.DataFrame(data)
    print('Dataframe Created Successfully!')

    # Authenticate with Google Sheets
    gc = authenticate_google_sheets()
    print('Authenticating with Google Sheets...')
    print(f'Result: {gc}')

    # name for the worksheet
    sheet_name = 'Energia Power Data'

    # Create or update the worksheet with the data
    create_or_update_worksheet(gc, sheet_name, df_power)

    # save to csv
    df_power.to_csv('power_data.csv', index=False)
    return df_power


generate_power_data(2015, 5)
