from django.urls import path
from payments import views

urlpatterns=[
    path('payLink/',views.AlipayAPIView.as_view()),
    path('payResoult/',views.AlipayResultAPIView.as_view())
]