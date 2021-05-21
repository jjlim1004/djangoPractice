from django.shortcuts import render, get_object_or_404

# Create your views here.
from rest_framework import viewsets, status
from myapp.serializers import PostSerializer
from myapp.models import Post

from rest_framework.response import Response
from rest_framework.views import APIView


# dict to json
# json.dumps(dictData)

# json to dict
# json.loads(jsonData)
class PostListAPIView(APIView):
    def get(self, request):
        serializer = PostSerializer(Post.objects.all(), many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class PostDetailAPIView(APIView):
    def get_object(self, pk):
        return get_object_or_404(Post, pk=pk)

    def get(self, request, pk, format=None):
        post = self.get_object(pk)
        serializer = PostSerializer(post)
        return Response(serializer.data)

    def put(self, request, pk):
        post = self.get_object(pk)
        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request, pk):
        post = self.get_object(pk)
        post.delete(post);
        return Response(status=status.HTTP_204_NO_CONTENT)