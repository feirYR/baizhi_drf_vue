from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
# Create your views here.
from rest_framework.generics import CreateAPIView

from order.models import Order
from order.serializers import OrderModelSerializer


class OrderAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Order.objects.filter(is_show=True,is_delete=False)
    serializer_class = OrderModelSerializer