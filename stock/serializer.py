from rest_framework import serializers

from .models import Kospi, Stock_information, Content


class KospiSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(user_url=True)

    class Meta:
        model = Kospi
        fields = '__all__'


class stockInformationSerializer(serializers.ModelSerializer):
    stock_code = serializers.CharField(max_length=100)
    stock_name = serializers.CharField(max_length=100)
    stock_price = serializers.CharField(max_length=100)
    stock_kind = serializers.CharField(max_length=100)

    class Meta:
        model = Stock_information
        fields = '__all__'

class ContentSerailizer(serializers.ModelSerializer):
    class Meta:
        model = Content
        fields = '__all__'