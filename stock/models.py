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



class Content(models.Model):
    title = models.CharField(max_length=20, null=True)
    content = models.CharField(max_length=30, null=True)
    image = models.ImageField(blank=True, null=True, upload_to="uploads")