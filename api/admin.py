from django.contrib import admin
from .models import *
# Register your models here.
class Items(admin.ModelAdmin):
    fields = ['name', 'stock', 'location', 'image', 'description', 'code', 'color']
    
admin.site.register(Item, Items)