from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.filters import OrderingFilter, SearchFilter

from .models import Customer, Staff
from .serializers import CustomerSerializer, StaffSerializer


class StaffViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Staff model.

    Provides CRUD operations for staff data with name search.
    """

    queryset = Staff.objects.select_related("store", "address").all()
    serializer_class = StaffSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["store", "active"]
    search_fields = ["first_name", "last_name", "email", "username"]
    ordering_fields = ["staff_id", "first_name", "last_name"]
    ordering = ["staff_id"]


class CustomerViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Customer model.

    Provides CRUD operations for customer data with search and filtering.
    """

    queryset = Customer.objects.select_related("store", "address").all()
    serializer_class = CustomerSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["store", "activebool"]
    search_fields = ["first_name", "last_name", "email"]
    ordering_fields = ["customer_id", "first_name", "last_name", "create_date"]
    ordering = ["customer_id"]
