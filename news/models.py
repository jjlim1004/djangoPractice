from django.db import models


# Create your models here.
class News(models.Model):
    keyword = models.TextField(default='TextField')
    title = models.TextField()
    url = models.TextField()


