from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^$', home_views),
    url(r'^test/', test),
]