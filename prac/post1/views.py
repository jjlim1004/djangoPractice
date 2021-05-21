from django.shortcuts import render
from rest_framework import viewsets
from .models import Post
from .serializers import PostSerializer


class PostViewSet(viewsets.ModelViewSet):
    # queryset = Post.objects.all()
    # post = Post.objects.all()
    # serializer = PostSerializer(post, many=True)
    # print(serializer.data)