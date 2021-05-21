from rest_framework import serializers
from .models import User


# django rest framework에서는 serializer 를 제공해주는데
# 이 serializer는 request 로 받은 data 를 역직렬화 하여 db에 반영하고
# response로 사용될 data를 다시 직렬화 해서 json이나 xml로 바꿔준다.
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # 모델 user 의 모든 field를 serializer 함
        fields = '__all__'
