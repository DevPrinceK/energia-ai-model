import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import random

import gspread
from google.oauth2 import service_account
from google.oauth2.service_account import Credentials
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics, permissions, status


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

def read_data_from_worksheet(gc, sheet_name):
    try:
        # Open the Google Sheet
        worksheet = gc.open(sheet_name).sheet1

        # Get all values from the worksheet as a list of lists
        data = worksheet.get_all_values()

        # Convert the data to a Pandas DataFrame (if needed)
        df = pd.DataFrame(data[1:], columns=data[0])  # Assuming the first row contains column headers

        return df

    except gspread.exceptions.SpreadsheetNotFound:
        print(f"Worksheet '{sheet_name}' not found.")
        return None


class PowerByAllRegionsAPI(APIView):
    '''Returns the average power consumption and generation by all regions'''

    def get(self, request, *args, **kwargs):
        # Read the data from the Google Sheet
        gc = authenticate_google_sheets()
        df = read_data_from_worksheet(gc, 'Energia Power Data')

        # Ensure 'Power_Consumption_MWh' and 'Power_Generation_MWh' columns are numeric
        df['Power_Consumption_MWh'] = pd.to_numeric(df['Power_Consumption_MWh'], errors='coerce')
        df['Power_Generation_MWh'] = pd.to_numeric(df['Power_Generation_MWh'], errors='coerce')

        # Group by Region and calculate the average power consumption and generation
        df_grouped = df.groupby('Region').agg({
            'Power_Consumption_MWh': 'mean',
            'Power_Generation_MWh': 'mean'
        }).reset_index()

        # Prepare the response in the desired JSON format
        response = [
            {
                "region": region,
                "power_consumption": power_consumption,
                "power_generation": power_generation
            }
            for region, power_consumption, power_generation in zip(
                df_grouped['Region'],
                df_grouped['Power_Consumption_MWh'],
                df_grouped['Power_Generation_MWh']
            )
        ]

        return Response(response)



class PowerBySingleRegionAPI(APIView):
    '''Returns the power consumption and generation for a single region'''

    def get(self, request, *args, **kwargs):
        # Read the data from the Google Sheet
        gc = authenticate_google_sheets()
        df = read_data_from_worksheet(gc, 'Energia Power Data')

        # Ensure 'Power_Consumption_MWh' and 'Power_Generation_MWh' columns are numeric
        df['Power_Consumption_MWh'] = pd.to_numeric(df['Power_Consumption_MWh'], errors='coerce')
        df['Power_Generation_MWh'] = pd.to_numeric(df['Power_Generation_MWh'], errors='coerce')

        # Get the region parameter from the request's data
        region = request.data.get('region')

        if not region:
            return Response({"error": "Region parameter is missing in the request body"}, status=status.HTTP_400_BAD_REQUEST)

        # Filter the DataFrame for the specified region
        region_data = df[df['Region'] == region]

        if region_data.empty:
            return Response({"error": f"No data found for region '{region}'"}, status=status.HTTP_404_NOT_FOUND)

        # Calculate the average power consumption and generation for the specified region
        avg_power_consumption = region_data['Power_Consumption_MWh'].mean()
        avg_power_generation = region_data['Power_Generation_MWh'].mean()

        # Prepare the response in the desired JSON format
        response = {
            "region": region,
            "power_consumption": avg_power_consumption,
            "power_generation": avg_power_generation
        }

        return Response(response)
    
class PowerByDistrictsInRegionAPI(APIView):
    '''Returns power consumption by districts in a specified region'''

    def post(self, request, *args, **kwargs):
        # Read the data from the Google Sheet
        gc = authenticate_google_sheets()
        df = read_data_from_worksheet(gc, 'Energia Power Data')

        # Ensure 'Power_Consumption_MWh'and 'Power_Generation_MWh' column is numeric
        df['Power_Consumption_MWh'] = pd.to_numeric(df['Power_Consumption_MWh'], errors='coerce')
        df['Power_Generation_MWh'] = pd.to_numeric(df['Power_Generation_MWh'], errors='coerce')

        # Get the region parameter from the request's data
        region = request.data.get('region')

        if not region:
            return Response({"error": "Region parameter is missing in the request body"}, status=status.HTTP_400_BAD_REQUEST)

        # Filter the DataFrame for the specified region
        region_data = df[df['Region'] == region]

        if region_data.empty:
            return Response({"error": f"No data found for region '{region}'"}, status=status.HTTP_404_NOT_FOUND)

        # Group by District within the specified region and calculate the sum of power consumption
        district_power_consumption = region_data.groupby('District')['Power_Consumption_MWh'].sum().reset_index()
        district_power_generation = region_data.groupby('District')['Power_Generation_MWh'].sum().reset_index()

        # Prepare the response in the desired JSON format
        response = [
            {
                "district": district,
                "power_consumption": power_consumption,
                "power_generation": power_generation,
            }
            for district, power_consumption, power_generation in zip(
                district_power_consumption['District'],
                district_power_consumption['Power_Consumption_MWh'],
                district_power_generation['Power_Generation_MWh'],
            )
        ]

        return Response(response)
    

class PowerByTownInRegion(APIView):
    '''Returns power consumption and generation for a town in a specified region'''

    def post(self, request, *args, **kwargs):
        # Read the data from the Google Sheet
        gc = authenticate_google_sheets()
        df = read_data_from_worksheet(gc, 'Energia Power Data')

        # Ensure 'Power_Consumption_MWh' and 'Power_Generation_MWh' columns are numeric
        df['Power_Consumption_MWh'] = pd.to_numeric(df['Power_Consumption_MWh'], errors='coerce')
        df['Power_Generation_MWh'] = pd.to_numeric(df['Power_Generation_MWh'], errors='coerce')

        # Get the region and town parameters from the request's data
        region = request.data.get('region')
        town = request.data.get('town')

        if not region or not town:
            return Response({"error": "Both region and town parameters are required in the request body"}, status=status.HTTP_400_BAD_REQUEST)

        # Filter the DataFrame for the specified region and town
        town_data = df[(df['Region'] == region) & (df['Town'] == town)]

        if town_data.empty:
            return Response({"error": f"No data found for region '{region}' and town '{town}'"}, status=status.HTTP_404_NOT_FOUND)

        # Calculate the sum of power consumption and generation for the specified town
        total_power_consumption = town_data['Power_Consumption_MWh'].sum()
        total_power_generation = town_data['Power_Generation_MWh'].sum()

        # Prepare the response in the desired JSON format
        response = {
            "region": region,
            "town": town,
            "power_consumption": total_power_consumption,
            "power_generation": total_power_generation
        }

        return Response(response)


class PowerByGridInRegion(APIView):
    '''Returns power consumption and generation for a grid in a specified region'''

    def post(self, request, *args, **kwargs):
        # Read the data from the Google Sheet
        gc = authenticate_google_sheets()
        df = read_data_from_worksheet(gc, 'Energia Power Data')

        # Ensure 'Power_Consumption_MWh' and 'Power_Generation_MWh' columns are numeric
        df['Power_Consumption_MWh'] = pd.to_numeric(df['Power_Consumption_MWh'], errors='coerce')
        df['Power_Generation_MWh'] = pd.to_numeric(df['Power_Generation_MWh'], errors='coerce')

        # Get the region and town parameters from the request's data
        region = request.data.get('region')
        grid = request.data.get('grid')

        if not region or not grid:
            return Response({"error": "Both region and grid parameters are required in the request body"}, status=status.HTTP_400_BAD_REQUEST)

        # Filter the DataFrame for the specified region and town
        town_data = df[(df['Region'] == region) & (df['Grid'] == grid)]

        if town_data.empty:
            return Response({"error": f"No data found for region '{region}' and grid '{grid}'"}, status=status.HTTP_404_NOT_FOUND)

        # Calculate the sum of power consumption and generation for the specified town
        total_power_consumption = town_data['Power_Consumption_MWh'].sum()
        total_power_generation = town_data['Power_Generation_MWh'].sum()

        # Prepare the response in the desired JSON format
        response = {
            "region": region,
            "grid": grid,
            "power_consumption": total_power_consumption,
            "power_generation": total_power_generation
        }

        return Response(response)