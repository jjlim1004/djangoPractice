from django.db import models


# Create your models here.
class Post(models.Model):
    text = models.TextField()
    dateTime = models.DateTimeField(auto_now_add=True)
    date = models.DateField(auto_now=True)


class Content(models.Model):
    title = models.CharField(max_length=20, null=True)
    content = models.CharField(max_length=30, null=True)
    image = models.ImageField(blank=True, null=True, upload_to="uploads")
