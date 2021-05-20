from django.db import models


# Create your models here.
class News(models.Model):
    title = models.TextField()
    url = models.TextField()

