from django.urls import path
from irnuscrawler_app import views

urlpatterns = [
    path('', views.index, name='index'),
]