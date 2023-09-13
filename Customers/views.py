from .models import Customer
from .serializers import CustomerSerializer
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse
from rest_framework import status
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404

#Customer API View
class CustomerAPIView(APIView):
    serializer_class = CustomerSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        """POST request function to create a new Customer object"""

        try:
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return JsonResponse({"status":status.HTTP_201_CREATED, "message": "Customer Created Successfully!", "results": serializer.data})
            else:
                return JsonResponse({"status":status.HTTP_400_BAD_REQUEST, "message": "An Error Occured!", "results": serializer.errors})
        except Exception as e:
            return JsonResponse({"status":status.HTTP_400_BAD_REQUEST, "message": "An Error Occured!", "results": {"error": str(e)}})

    def get(self, request, pk=None):
        """GET request function to either retrieve a given Customer object or list all Customers objects"""

        if pk:
            # if the customer's primary key is part of the request
            try:
                customer_obj = get_object_or_404(Customer, id=pk)
                serializer =self.serializer_class(customer_obj)
                if serializer.is_valid:
                    return JsonResponse({"status":status.HTTP_200_OK, "message": "Customer Details Retrieved Successfully!", "results": serializer.data})
                else:
                    return JsonResponse({"status":status.HTTP_400_BAD_REQUEST, "message": "An Error Occured!", "results": serializer.errors})
            except Exception as e:
                return JsonResponse({"status":status.HTTP_400_BAD_REQUEST, "message": "An Error Occured!", "results": {"error": str(e)}})
        else:
            # if the customer's primary key is not part of the request
            try:
                customer_objs = Customer.objects.all().order_by("-date_created")
                serializer =self.serializer_class(customer_objs, many=True, context={'request': request})
                if serializer.is_valid:
                    return JsonResponse({"status":status.HTTP_200_OK, "message": "Customers Retrieved Successfully!", "results": serializer.data})
                else:
                    return JsonResponse({"status":status.HTTP_400_BAD_REQUEST, "message": "An Error Occured!", "results": serializer.errors})
            except Exception as e:
                return JsonResponse({"status":status.HTTP_400_BAD_REQUEST, "message": "An Error Occured!", "results": {"error": str(e)}})

    def patch(self, request, pk=None):
        """PATCH request function to update a given Customer object"""

        try:
            customer_obj = get_object_or_404(Customer, id=pk)
            serializer =self.serializer_class(instance=customer_obj, data=request.data, partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return JsonResponse({"status":status.HTTP_200_OK, "message": "Customer Details Updated Successfully!", "results": serializer.data})
            else:
                return JsonResponse({"status":status.HTTP_400_BAD_REQUEST, "message": "An Error Occured!", "results": serializer.errors})
        except Exception as e:
            return JsonResponse({"status":status.HTTP_400_BAD_REQUEST, "message": "An Error Occured!", "results": {"error": str(e)}})
        
    def delete(self, pk=None):
        """DELETE request function to delete a given Customer object"""

        try:
            customer_obj = get_object_or_404(Customer, id=pk)
            customer_obj.delete()
            return JsonResponse({"status":status.HTTP_204_NO_CONTENT, "message": "Customer Details Deleted Successfully!"})
        except Exception as e:
            return JsonResponse({"status":status.HTTP_400_BAD_REQUEST, "message": "An Error Occured!", "results": {"error": str(e)}})