from order import views
from django.urls import path
urlpatterns=[
    path('courseOrder/',views.OrderAPIView.as_view()),
]