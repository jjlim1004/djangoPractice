from django.urls import path

from . import views

app_name = 'stock'

urlpatterns = [
    path('', views.stock, name='stock'),
    path('kospi/', views.stock_graph.as_view(), name='kospi'),
    path('stocklist/', views.stock_information.as_view(), name='stock_inform'),
    path('stock_detail/', views.stock_detail.as_view(), name='stock_detail'),
]
