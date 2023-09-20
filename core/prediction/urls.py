from django.urls import path
from .views import prediction
from .views import analysis

urlpatterns = [
    path('', prediction.Overview.as_view(), name="overview"),
    path('predict-outage/', prediction.PredictPowerOutage.as_view()),
    path('power-by-all-regions/', analysis.PowerByAllRegionsAPI.as_view()),
    path('power-by-single-region/', analysis.PowerBySingleRegionAPI.as_view()),
    path('power-by-districts-in-region/', analysis.PowerByDistrictsInRegionAPI.as_view()),
    path('power-by-town-in-region/', analysis.PowerByTownInRegion.as_view()),
    path('power-by-grid-in-region/', analysis.PowerByGridInRegion.as_view()),
]
