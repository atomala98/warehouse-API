from rest_framework import serializers
from .models import *

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ('id', 'name', 'stock', 'location', 'image', 'description', 'code', 'color')
        
class UpdateStockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ('stock', 'code')
        
class CreateItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ('id', 'name', 'location', 'image', 'description', 'code', 'color')