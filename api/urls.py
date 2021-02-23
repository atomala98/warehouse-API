from django.urls import path
from .views import home, ItemView, SingleItemView, SingleItemDelivery, AddItem


urlpatterns = [
    path('home', home),
    path('items', ItemView.as_view()),
    path('get-item', SingleItemView.as_view()),
    path('change-stock', SingleItemDelivery.as_view()),
    path('add-item', AddItem.as_view()),
]
