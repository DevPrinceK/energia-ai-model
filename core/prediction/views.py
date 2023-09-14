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