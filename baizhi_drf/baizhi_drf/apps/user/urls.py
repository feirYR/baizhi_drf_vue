from django.urls import path
from django.contrib.auth.backends import ModelBackend
from rest_framework_jwt.views import obtain_jwt_token
from user import views
urlpatterns=[
    path('login/',obtain_jwt_token),
    path('captche/',views.Captche.as_view())
]