
from django.urls import path
from .views import *


urlpatterns = [
    path('list', OrdersView.as_view()),
    path('create', CreateOrder.as_view()),
    path('finish', FinishOrder.as_view()),
    path('add-item', AddToOrder.as_view()),
    path('details', DetailsView.as_view()),
    path('check-item', CheckItem.as_view()),
    path('complete', CompleteCollection.as_view()),
]
