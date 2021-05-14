from django.urls import path

from . import views

app_name = 'stock'

urlpatterns = [
    path('', views.stock, name='stock'),
    path('kospi/', views.kospi, name='kospi'),
]
