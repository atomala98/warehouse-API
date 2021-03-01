from rest_framework import serializers
from .models import *
from api.serializers import ItemSerializer

class DetailsSerializer(serializers.ModelSerializer):
    item = ItemSerializer()

    class Meta:
        model = Details
        fields = ('item', 'amount')


class OrderSerializer(serializers.ModelSerializer):
    item = DetailsSerializer(source='details_set', many=True)
    depth = 2
    class Meta:
        model = Order
        fields = ('id', 'number', 'deadline', 'status', 'item')
                
        
class OrderIDSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('number', )
        

class AddToOrderSerializer(serializers.ModelSerializer):
    code = serializers.IntegerField()
    amount = serializers.IntegerField()
    
    class Meta:
        model = Order
        fields = ('number', 'code', 'amount')