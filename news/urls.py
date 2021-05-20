from django.urls import path

from . import views
from .views import NewsView

app_name = 'news'
urlpatterns = [
    path('', views.NewsView.as_view(), name='news_list'),
    path('<str:keyword>/', views.NewsView.as_view(), name='news')
]
