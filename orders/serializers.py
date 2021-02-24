from rest_framework import serializers
from .models import *
from api.serializers import ItemCodeSerializer

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('id', 'number', 'deadline', 'status', 'items')
        
        
class OrderIDSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('number', )
        