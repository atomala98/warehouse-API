from django.shortcuts import render
from .serializers import *
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics, status

# Create your views here.
def home(request):
    html = "<html><body>Home</body></html>"
    return HttpResponse(html)

class ItemView(generics.ListAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    
    
class SingleItemView(APIView):
    serializer_class = ItemSerializer
    lookup_url_kwarg = 'code'
    
    def get(self, request, format=None):
        code = request.GET.get(self.lookup_url_kwarg)
        item = Item.objects.filter(code=code).first()
        if item:
            data = self.serializer_class(item).data
            return Response(data, status=status.HTTP_200_OK)
        return Response({}, status=status.HTTP_400_BAD_REQUEST)
    
    
class SingleItemDelivery(APIView):
    serializer_class = UpdateStockSerializer
    
    def patch(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            code = serializer.data.get('code')
            item = Item.objects.filter(code=code).first()
            if item:
                item.stock += int(serializer.data.get('stock'))
                item.save(update_fields=['stock'])
                return Response(ItemSerializer(item).data, status=status.HTTP_200_OK)
            return Response({}, status=status.HTTP_400_BAD_REQUEST)
        return Response({}, status=status.HTTP_400_BAD_REQUEST)


class AddItem(APIView):
    serializer_class = CreateItemSerializer
    
    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        print(serializer.is_valid())
        if serializer.is_valid():
            name = serializer.data.get('name')
            location = serializer.data.get('location')
            image = serializer.data.get('image')
            description = serializer.data.get('description')
            code = serializer.data.get('code')
            color = serializer.data.get('color')
            item = Item.objects.filter(code=code).first()
            if item:
                item.name = name
                item.location = location
                item.image = image
                item.description = description
                item.color = color
                item.save(update_fields=['name', 'location', 'image', 'description', 'color'])
                return Response(ItemSerializer(item).data, status=status.HTTP_200_OK)
            else:
                item = Item(name=name, location=location, image=image, description=description, code=code, color=color)
                item.save()       
                return Response(ItemSerializer(item).data, status=status.HTTP_200_OK)
            return Response(status=status.HTTP_400_BAD_REQUEST)  
        return Response(status=status.HTTP_404_NOT_FOUND)  
    