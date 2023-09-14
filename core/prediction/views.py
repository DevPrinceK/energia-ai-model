import pickle
import pandas as pd
from sklearn.calibration import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from django.shortcuts import render
from knox.views import LoginView as KnoxLoginView
from rest_framework import generics, permissions, status
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.response import Response
from rest_framework.views import APIView


class Overview(APIView):
    '''API Overview'''
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        '''Returns the overview of the api - docs of the api'''
        return Response({
            "message": "Energia-AI API"
        }, status=status.HTTP_200_OK)


class PredictPowerOutage(APIView):
    '''Predicts posible power outages'''
    def post(self, request):
        # Read the request data
        data = request.data.get('data')

        # Convert the data to a pandas DataFrame
        df = pd.DataFrame(data)
        
        # Convert the 'Date' column to datetime
        df['Date'] = pd.to_datetime(df['Date'])
        df['Year'] = df['Date'].dt.year
        df['Month'] = df['Date'].dt.month
        df['Day'] = df['Date'].dt.day
        df['DayOfWeek'] = df['Date'].dt.dayofweek
        
        with open("C:/Users/branana/Desktop/Github Repos/energia-ai-model/core/prediction/label_encoders.pkl", "rb") as f:
            label_encoders = pickle.load(f)

        # Load the trained model using pickle
        with open("C:/Users/branana/Desktop/Github Repos/energia-ai-model/core/prediction/rf_prediction_model.pkl", "rb") as f:
            model = pickle.load(f)
            
        # Convert categorical variables to numerical using Label Encoding
        categorical_cols = ['Region', 'District', 'Town', 'Grid']
        for col in categorical_cols:
            le = label_encoders[col]
            df[col] = le.transform(df[col])

        # ignore the 'Date' column
        df.drop('Date', axis=1, inplace=True)
        
        # Perform predictions
        predictions = model.predict(df)

        # Prepare the response
        response = {
            'predictions': ["No" if not bool(i) else "Yes" for i in predictions.tolist()]
        }

        return Response(response)
