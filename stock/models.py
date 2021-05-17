from django.db import models


# Create your models here.
class Kospi(models.Model):
    image = models.ImageField(default='static/img/kospi.png')
