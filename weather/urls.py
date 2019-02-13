from django.conf.urls import url
from .views import *
urlpatterns = [
    url(r'^$', weather_00_views),
]