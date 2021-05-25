from django.urls import path

from . import views
from .views import NewsView

app_name = 'news'
urlpatterns = [
    path('', views.form, name='news_form'),
    # path('', views.NewsView.as_view(), name='news_list'),
    path('news/', views.NewsView.as_view(), name='news'),
]
