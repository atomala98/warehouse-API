from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import *
from .models import *
# Create your views here.

class OrdersView(generics.ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    
    
class CreateOrder(APIView):
    
    def post(self, request, format=None):
        order = Order()
        order.save()
        return Response(OrderSerializer(order).data, status=status.HTTP_200_OK)
    

class FinishOrder(APIView):
    serializer_class = OrderIDSerializer
    
    def delete(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        print(serializer.is_valid())
        if serializer.is_valid():
            number = serializer.data.get('number')
            order = Order.objects.filter(number=number).first()
            if order:
                order.delete()
                return Response({}, status=status.HTTP_200_OK)
            return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)
        return Response({}, status=status.HTTP_404_NOT_FOUND)    