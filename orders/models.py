from django.db import models
from api.models import Item
from django.utils import timezone
from datetime import timedelta
from random import randint
# Create your models here.

def order_number():
    length = 6
    while True:
        number = randint(10**5, 10**6 - 1)
        if not Order.objects.filter(number=number).first():
            break
    return number

class Order(models.Model):
    number = models.IntegerField(default=order_number)
    deadline = models.DateTimeField(default=timezone.now()+timedelta(days=5))
    status = models.CharField(default="Started", max_length=20)
    items = models.ManyToManyField(Item,
        through='Details')
    
class Details(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    amount_to_check = models.IntegerField(default=0)
    amount = models.IntegerField(default=1)