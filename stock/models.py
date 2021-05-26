from django.db import models


# Create your models here.
class Kospi(models.Model):
    date = models.DateField
    imageUrl = models.TextField(default='/stock/static/img/kospi.png')

class Stock_information(models.Model):
    stock_code = models.TextField
    stock_name = models.TextField
    stock_price = models.TextField
    stock_kind = models.TextField