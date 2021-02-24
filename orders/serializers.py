from rest_framework import serializers
from .models import *
from api.serializers import ItemSerializer

class OrderSerializer(serializers.ModelSerializer):
    items = ItemSerializer(read_only=True, many=True)
    
    class Meta:
        model = Order
        fields = ('id', 'number', 'deadline', 'status', 'items')
        
        
class OrderIDSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('number', )
        

class AddToOrderSerializer(serializers.ModelSerializer):
    code = serializers.IntegerField()
    
    class Meta:
        model = Order
        fields = ('number', 'code')