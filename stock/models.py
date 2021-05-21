from django.db import models


# Create your models here.
class Kospi(models.Model):
    date = models.DateField
    imageUrl = models.TextField(default='/stock/static/img/kospi.png')
