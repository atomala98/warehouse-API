from django.shortcuts import render
from django.db.models import Q
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import *
from .models import *
# Create your views here.

class DetailsView(generics.ListAPIView):
    queryset = Details.objects.all()
    serializer_class = DetailsSerializer
    

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
        if serializer.is_valid():
            number = serializer.data.get('number')
            order = Order.objects.filter(number=number).first()
            if order:
                order.delete()
                return Response({}, status=status.HTTP_200_OK)
            return Response({"Message": f"No order {number}"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"Message": "Invalid data."}, status=status.HTTP_404_NOT_FOUND)    
    

class AddToOrder(APIView):
    serializer_class = AddToOrderSerializer
    
    def patch(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            number = serializer.data.get('number')
            code = serializer.data.get('code')
            amount = serializer.data.get('amount')
            order = Order.objects.filter(number=number).first()
            item = Item.objects.filter(code=code).first()
            print(order, item)
            if order and item:
                if item not in order.items.all():
                    detail = Details(order=order, item=item, amount=amount)
                    detail.save()
                    return Response({}, status=status.HTTP_200_OK)
                else:
                    detail = Details.objects.filter(Q(item=item)|Q(order=order)).first()
                    detail.amount += amount
                    detail.save(update_fields=['amount'])
                    return Response({}, status=status.HTTP_400_BAD_REQUEST)
            return Response({}, status=status.HTTP_400_BAD_REQUEST)
        return Response({}, status=status.HTTP_404_NOT_FOUND)
    
    
class CheckItem(APIView):
    serializer_class = CheckItemSerializer
    
    def patch(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            number = serializer.data.get('number')
            code = serializer.data.get('code')
            amount_to_check = serializer.data.get('amount_to_check')
            order = Order.objects.filter(number=number).first()
            item = Item.objects.filter(code=code).first()
            print(amount_to_check, order.number, item.code)
            if order and item:
                if item not in order.items.all():
                    return Response({"Message": "Item not in order"}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    detail = Details.objects.filter(Q(item=item)&Q(order=order)).first()
                    print(detail.order.number)
                    if detail.amount < detail.amount_to_check + amount_to_check:
                        return Response({"Message": "Too many items."}, status=status.HTTP_400_BAD_REQUEST)
                    else:
                        detail.amount_to_check += amount_to_check
                        detail.save(update_fields=['amount_to_check'])
                        if detail.amount_to_check == detail.amount:
                            return Response({"Message": "All items collected."}, status=status.HTTP_400_BAD_REQUEST)
                        else:
                            return Response({"Message": f"{amount_to_check} items collected."}, status=status.HTTP_400_BAD_REQUEST)
            return Response({"Message": "Invalid data."}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"Message": "Invalid data."}, status=status.HTTP_404_NOT_FOUND)
    
    
class CompleteCollection(APIView):
    serializer_class = OrderIDSerializer
    
    def patch(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            number = serializer.data.get('number')
            order = Order.objects.filter(number=number).first()
            if order and order.status == "Started":
                details = Details.objects.filter(order=order)
                for detail in details:
                    if detail.amount_to_check != detail.amount:
                        return Response({"Message": "Collecting not completed!"})
                for detail in details:
                    detail.amount_to_check = 0
                    detail.save(update_fields=['amount_to_check'])
                order.status = 'Collected'
                order.save(update_fields=['status'])
                return Response({"Message": f"Order {number} collecting completed."})
        return Response({"Message": "Something went wrong."}, status=status.HTTP_400_BAD_REQUEST)
    
    
class CompleteVerification(APIView):
    serializer_class = OrderIDSerializer
    
    def patch(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            number = serializer.data.get('number')
            order = Order.objects.filter(number=number).first()
            if order and order.status == "Collected":
                details = Details.objects.filter(order=order)
                for detail in details:
                    if detail.amount_to_check != detail.amount:
                        return Response({"Message": "Collecting not completed!"})
                for detail in details:
                    detail.amount_to_check = 0
                    detail.save(update_fields=['amount_to_check'])
                order.status = 'Verified'
                order.save(update_fields=['status'])
                return Response({"Message": f"Order {number} collecting completed."})
        return Response({"Message": "Something went wrong."}, status=status.HTTP_400_BAD_REQUEST)
    
    
class OrderShipped:
    serializer_class = OrderIDSerializer
    
    def patch(self, request, format=None):
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                number = serializer.data.get('number')
                order = Order.objects.filter(number=number).first()
                if order and order.status == "Verified":
                    order.status = 'Shipped'
                    order.save(update_fields=['status'])
                    return Response({"Message": f"Order {number} collecting completed."})
            return Response({"Message": "Something went wrong."}, status=status.HTTP_400_BAD_REQUEST)