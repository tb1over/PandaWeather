from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^$', retrieve_views),
    url(r'^retrieve/', retrieve_03_views),
    url(r'^retrieve_01/', retrieve_02_views),
    url(r'^retrieve_02/', retrieve_04_views),
]