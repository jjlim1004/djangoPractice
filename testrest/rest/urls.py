from django.db import router
from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('post', views.PostViewSet)

#path가 '' 일 때 host/blog/dd 이면 PostViewSet이 작동
# router.register('dd', views.PostViewSet) #host/blog/
#host/blog/1 이렇게 하면 아이디 1에 대한 결과를 get으로 받아옴

urlpatterns = [
    path('', include(router.urls))  #host/blog/
    # path('posturl/', include(router.urls)) # host/blog/posturl/
]
