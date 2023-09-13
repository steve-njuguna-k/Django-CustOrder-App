from django.urls import path
from Customers.views import CustomerAPIView

urlpatterns = [
    path('v1/customers', CustomerAPIView.as_view(), name='list_create_customers'),
    path('v1/customers/<int:pk>', CustomerAPIView.as_view(), name="update_delete_customers"),
]