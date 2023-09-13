from django.urls import path
from Customers.views import CustomerAPIView
from Items.views import ItemAPIView
from Orders.views import OrderAPIView
from Auth.views import RegistrationAPIView, LoginAPIView, LogoutAPIView

urlpatterns = [
    path('v1/login', LoginAPIView.as_view(), name='log_in_user'),
    path('v1/register', RegistrationAPIView.as_view(), name='register_user'),
    path('v1/logout', LogoutAPIView.as_view(), name='logout_user'),

    path('v1/customers', CustomerAPIView.as_view(), name='list_create_customers'),
    path('v1/customers/<int:pk>', CustomerAPIView.as_view(), name="update_delete_customers"),

    path('v1/items', ItemAPIView.as_view(), name="list_create_items"),
    path('v1/items/<int:pk>', ItemAPIView.as_view(), name="update_delete_items"),

    path('v1/orders', OrderAPIView.as_view(), name="list_create_orders"),
    path('v1/orders/<int:pk>', OrderAPIView.as_view(), name="update_delete_orders"),
]