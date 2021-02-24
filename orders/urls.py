
from django.urls import path
from .views import OrdersView, CreateOrder, FinishOrder


urlpatterns = [
    path('list', OrdersView.as_view()),
    path('create', CreateOrder.as_view()),
    path('finish', FinishOrder.as_view()),
]
