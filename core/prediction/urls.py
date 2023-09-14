from django.urls import path
from . import views

urlpatterns = [
    path('', views.Overview.as_view(), name="overview")
]
