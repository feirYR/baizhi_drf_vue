from django.urls import path
from django.contrib.auth.backends import ModelBackend
from rest_framework_jwt.views import obtain_jwt_token
from user import views
urlpatterns=[
    path('login/',obtain_jwt_token),
    path('captche/',views.Captche.as_view()),
    path('check/<str:phone>',views.CheckPhoneAPIView.as_view()),
    path('sms/<str:phone>',views.SendmessageAPIView.as_view()),
    path('register/',views.RegisterCreateAPIView.as_view()),
    path('logout/<str:username>',views.LogoutAccountAPIView.as_view())
]