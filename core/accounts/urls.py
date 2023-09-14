from django.urls import path
from knox import views as knox_views
from . import views


urlpatterns = [
    path('login/',  views.LoginAPI.as_view(), name="login"),
    path('logout/', knox_views.LogoutView.as_view(), name='logout'),
]
