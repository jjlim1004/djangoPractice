from rest_framework import viewsets
from rest_framework.response import Response

from .models import Post
from .serializers import PostSerializer
# https://inma.tistory.com/88?category=984128

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    # 여기 까지만 해줘도 기본적인 crud는 된다.

    # get_queryset(self) 를 오버라이딩
    # GET 방식 /blog/post/
    # GET 방식 /blog/post/?search=
    def get_queryset(self):
        qs = super().get_queryset()

        search = self.request.query_params.get('search', '')
        if search:
            qs = qs.filter(message__icontains=search)

        return qs

    # GET 방식 /blog/post/get_django/
    @list_route() #/prefix/함수명 == /blog/post/get_django 로 GET  요청
    def get_django(self, request):
        qs = self.get_queryset().filter(message__icontains='django')
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)

    @detail_route(methods=['patch'])
    #patch 방식 요청에 대한 매핑.
    #하나에 데이터에 대한 작업을 수행시에 사용
    #/prefix/{pk}/함수명 ==  /blog/post/{pk}/set_modified
    def set_modified(self, request, pk):
        instance = self.get_object()
        instance.message = instance.message + '(modified)'
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)