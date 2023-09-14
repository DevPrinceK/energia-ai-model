from django.urls import path
from . import views

urlpatterns = [
    path('', views.Overview.as_view(), name="overview"),
    path('predict-outage/', views.PredictPowerOutage.as_view(), name="predict"),
]
