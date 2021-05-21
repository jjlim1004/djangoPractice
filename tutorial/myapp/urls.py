from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views


urlpatterns = [
    path('post/', views.PostListAPIView.as_view()),
    path('post/', views.PostDetailAPIView.as_view()),

]