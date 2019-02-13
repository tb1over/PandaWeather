from django.db import models

# Create your models here.
class User(models.Model):
    name = models.EmailField(primary_key=True)
    pwd = models.CharField(max_length=254)
    nickname = models.CharField(max_length=254)
    accept = models.IntegerField()
    city1 = models.CharField(max_length=60, default="默认:北京-北京")
    city2 = models.CharField(max_length=60, default="默认:北京-北京")
    city3 = models.CharField(max_length=60, default="默认:北京-北京")
    is_delete = models.BooleanField(default=0)