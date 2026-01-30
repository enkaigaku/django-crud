from django.core.exceptions import ValidationError as DjangoValidationError
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError as DRFValidationError
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.response import Response

from .models import Inventory, Payment, Rental
from .serializers import InventorySerializer, PaymentSerializer, RentalSerializer
from .services import RentalService


class InventoryViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Inventory model.

    Provides CRUD operations for inventory data with film and store relationships.
    """

    queryset = Inventory.objects.select_related("film", "store").all()
    serializer_class = InventorySerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["film", "store"]
    search_fields = ["film__title"]
    ordering_fields = ["inventory_id"]
    ordering = ["inventory_id"]


class RentalViewSet(viewsets.GenericViewSet):
    """
    ViewSet for Rental model.

    Only provides create and return operations via Service Layer.
    """

    queryset = Rental.objects.all()
    serializer_class = RentalSerializer

    def create(self, request, *args, **kwargs):
        """
        Create a new rental using the Service Layer.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            rental = RentalService.create_rental(
                customer_id=serializer.validated_data["customer"].customer_id,
                inventory_id=serializer.validated_data["inventory"].inventory_id,
                staff_id=serializer.validated_data["staff"].staff_id,
            )
        except DjangoValidationError as e:
            raise DRFValidationError(
                e.message_dict if hasattr(e, "message_dict") else e.messages
            )

        output_serializer = self.get_serializer(rental)
        headers = self.get_success_headers(output_serializer.data)
        return Response(
            output_serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    @action(detail=True, methods=["post"])
    def return_movie(self, request, pk=None):
        """
        Custom action to return a rented movie.
        """
        try:
            rental = RentalService.return_rental(pk)
        except DjangoValidationError as e:
            raise DRFValidationError(
                e.message_dict if hasattr(e, "message_dict") else e.messages
            )

        serializer = self.get_serializer(rental)
        return Response(serializer.data)


class PaymentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Payment model.

    Provides CRUD operations for payment data.
    """

    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["customer_id", "staff_id", "rental_id"]
    ordering_fields = ["payment_id", "payment_date", "amount"]
    ordering = ["-payment_date"]
