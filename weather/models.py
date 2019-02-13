from django.db import models

# Create your models here.
class Weather_now(models.Model):
    city = models.CharField(max_length=10, null=False,primary_key=True)
    weat_now = models.CharField(max_length=40, null=False)
    temp_now = models.CharField(max_length=40, null=False)
    humi_now = models.CharField(max_length=40, null=False)
    airq_now = models.CharField(max_length=40, null=False)
    rays_now = models.CharField(max_length=40, null=False)
    wind_now = models.CharField(max_length=40, null=False)
    time_now = models.CharField(max_length=20, null=False)

class Weather_tom(models.Model):
    city = models.ForeignKey(Weather_now)
    date_tom = models.CharField(max_length=40, null=False)
    weat_tom = models.CharField(max_length=40, null=False)
    temp_tom = models.CharField(max_length=40, null=False)
    airq_tom = models.CharField(max_length=40, null=False)
    wind_tom = models.CharField(max_length=40, null=False)