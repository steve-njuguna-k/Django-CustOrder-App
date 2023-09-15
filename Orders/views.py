from Customers.models import Customer
from .models import Order
from .serializers import OrderSerializer
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse
from rest_framework import status
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from core.services import send_sms
from Items.models import Item

#Order API View
class OrderAPIView(APIView):
    serializer_class = OrderSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        """POST request function to create a new Order object"""

        try:
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()

                customer = Customer.objects.get(id=serializer.data['customer'])
                
                send_sms(
                    "{} {}".format(serializer.data['customer_first_name'], serializer.data['customer_last_name']), 
                    serializer.data['item_name'], 
                    serializer.data['quantity'], 
                    serializer.data['total'],
                    customer.phone_number
                    )
                return JsonResponse({"status":status.HTTP_201_CREATED, "message": "Order Created Successfully! An SMS has been sent to the customer for delivery", "results": serializer.data})
            else:
                return JsonResponse({"status":status.HTTP_400_BAD_REQUEST, "message": "An Error Occured!", "results": serializer.errors})
        except Exception as e:
            return JsonResponse({"status":status.HTTP_400_BAD_REQUEST, "message": "An Error Occured!", "results": {"error": str(e)}})

    def get(self, request, pk=None):
        """GET request function to either retrieve a given Order object or list all Orders objects"""

        if pk:
            # if the order's primary key is part of the request
            try:
                order_obj = get_object_or_404(Order, id=pk)
                serializer =self.serializer_class(order_obj)
                if serializer.is_valid:
                    return JsonResponse({"status":status.HTTP_200_OK, "message": "Order Details Retrieved Successfully!", "results": serializer.data})
                else:
                    return JsonResponse({"status":status.HTTP_400_BAD_REQUEST, "message": "An Error Occured!", "results": serializer.errors})
            except Exception as e:
                return JsonResponse({"status":status.HTTP_400_BAD_REQUEST, "message": "An Error Occured!", "results": {"error": str(e)}})
        else:
            # if the order's primary key is not part of the request
            try:
                order_objs = Order.objects.all().order_by("-date_created")
                serializer =self.serializer_class(order_objs, many=True, context={'request': request})
                if serializer.is_valid:
                    return JsonResponse({"status":status.HTTP_200_OK, "message": "Orders Retrieved Successfully!", "results": serializer.data})
                else:
                    return JsonResponse({"status":status.HTTP_400_BAD_REQUEST, "message": "An Error Occured!", "results": serializer.errors})
            except Exception as e:
                return JsonResponse({"status":status.HTTP_400_BAD_REQUEST, "message": "An Error Occured!", "results": {"error": str(e)}})

    def patch(self, request, pk=None):
        """PATCH request function to update a given Order object"""

        try:
            order_obj = get_object_or_404(Order, id=pk)
            serializer =self.serializer_class(instance=order_obj, data=request.data, partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return JsonResponse({"status":status.HTTP_200_OK, "message": "Order Details Updated Successfully!", "results": serializer.data})
            else:
                return JsonResponse({"status":status.HTTP_400_BAD_REQUEST, "message": "An Error Occured!", "results": serializer.errors})
        except Exception as e:
            return JsonResponse({"status":status.HTTP_400_BAD_REQUEST, "message": "An Error Occured!", "results": {"error": str(e)}})
        
    def delete(self, pk=None):
        """DELETE request function to delete a given Order object"""

        try:
            order_obj = get_object_or_404(Order, id=pk)
            order_obj.delete()
            return JsonResponse({"status":status.HTTP_204_NO_CONTENT, "message": "Order Details Deleted Successfully!"})
        except Exception as e:
            return JsonResponse({"status":status.HTTP_400_BAD_REQUEST, "message": "An Error Occured!", "results": {"error": str(e)}})