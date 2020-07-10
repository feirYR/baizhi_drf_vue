from django.shortcuts import render

# Create your views here.
from rest_framework.generics import ListAPIView
from home.serializers import BnnerModelSerializer,NavModelSerializer
from home.models import Banner, Navigation


class BannerListAPIView(ListAPIView):
    queryset = Banner.objects.filter(is_show=True,is_delete=False).order_by('ordering')
    serializer_class = BnnerModelSerializer

class NavListAPIView(ListAPIView):
    queryset = Navigation.objects.filter(is_show=True,is_delete=False).order_by('ordering')
    serializer_class = NavModelSerializer