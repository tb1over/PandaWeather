from django.conf.urls import url
from .views import *

urlpatterns = [
    url(r'^$', register_views),
    url(r'^register_01/$', register_03_views),
    url(r'^register_02/$', register_02_views),
    url(r'^register_db/$', register_db_views),

]