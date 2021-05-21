from django.conf.urls import url
from django.contrib import admin
from django.db import router
from django.urls import path, include
from rest_framework import routers

from restPrac import views

router = routers.DefaultRouter()
router.register(r'persons', views.PersonViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('polls/', include('polls.urls')),
    path('books/', include('books.urls')),
    path('users/', include('api_user.urls'), name='api_user'),
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),


]
