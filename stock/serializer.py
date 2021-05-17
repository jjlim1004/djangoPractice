from rest_framework import serializers

from .models import Kospi


class KospiSerializer(serializers.HyperLinkedModelSerializer):
    image = serializers.ImageField(user_url=True)

    class Meta:
        model = Kospi
        fields = '__all__'
