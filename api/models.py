from django.db import models
import random
from django.utils import timezone
from datetime import timedelta


# Create your models here.
class Item(models.Model):
    name = models.CharField(max_length=30)
    stock = models.IntegerField(default=0)
    location = models.CharField(max_length=5)
    image = models.CharField(max_length=120)
    description = models.CharField(max_length=200)
    code = models.IntegerField()
    color = models.CharField(max_length=20)
    

class UncompletedOrder(models.Model):
    items = models.ManyToManyField(Item, through='OrderDetails')
    deadline = models.DateTimeField(default=timezone.now() + timedelta(days = 3))
    
    
class OrderDetails(models.Model):
    order = models.ForeignKey(UncompletedOrder, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    amount = models.IntegerField()