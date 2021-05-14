from django.contrib import admin
from django.urls import path, include

from . import views

app_name = 'api_user'
urlpatterns = [
    path('', views.UserView.as_view()),

]
