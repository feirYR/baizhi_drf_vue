from django.urls import path
from cart import views
urlpatterns=[
    path('cart/',views.CartViewSet.as_view({'post':'add_cart','get':'show_cart','patch':'select_cart',
                                            'delete':'del_cart','put':'course_expire'})),
    path('order/',views.CartViewSet.as_view({'get':'get_billCourse'})),
    # path('select_all/',views.CartViewSet.as_view({'post':'select_all_cart'}))

]