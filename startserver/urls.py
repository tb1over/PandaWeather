from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^startserver/password/onlyme/$', startserver_views)
    ]