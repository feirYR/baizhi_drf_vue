from django.urls import path
from cart import views
urlpatterns=[
    path('cart/',views.CartViewSet.as_view({'post':'add_cart','get':'show_cart','patch':'select_cart','delete':'del_cart'})),
    # path('show_cart/',views.CartViewSet.as_view({'post':'show_cart'}))
]