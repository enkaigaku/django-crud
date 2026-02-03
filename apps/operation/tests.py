from unittest.mock import MagicMock, patch

from django.core.exceptions import ValidationError
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIRequestFactory

from apps.account.models import Customer, Staff
from apps.operation.models import Inventory, Rental
from apps.operation.serializers import (
    InventorySerializer,
    PaymentSerializer,
    RentalSerializer,
)
from apps.operation.services import RentalService
from apps.operation.views import RentalViewSet


class RentalServiceTests(TestCase):
    def setUp(self):
        self.customer_mock = MagicMock(spec=Customer)
        self.customer_mock.activebool = True
        self.inventory_mock = MagicMock(spec=Inventory)
        self.staff_mock = MagicMock(spec=Staff)
        self.rental_mock = MagicMock(spec=Rental)

    @patch("apps.operation.services.transaction.atomic")
    @patch("apps.operation.services.Customer.objects.get")
    @patch("apps.operation.services.Inventory.objects.select_for_update")
    @patch("apps.operation.services.Staff.objects.get")
    @patch("apps.operation.services.Rental.objects.filter")
    @patch("apps.operation.services.Rental")
    def test_create_rental_success(
        self,
        mock_rental_cls,
        mock_rental_filter,
        mock_staff_get,
        mock_inventory_qs,
        mock_customer_get,
        mock_atomic,
    ):
        # Setup context manager for atomic
        mock_atomic.return_value.__enter__.return_value = None

        # Setup mocks
        mock_customer_get.return_value = self.customer_mock

        # Mocking Inventory.objects.select_for_update().get()
        mock_inventory_qs.return_value.get.return_value = self.inventory_mock

        mock_staff_get.return_value = self.staff_mock

        # Rental.objects.filter(...).exists() -> False (not rented)
        mock_rental_filter.return_value.exists.return_value = False

        mock_rental_instance = MagicMock()
        mock_rental_cls.return_value = mock_rental_instance

        # Execute
        result = RentalService.create_rental(1, 1, 1)

        # Assert
        self.assertEqual(result, mock_rental_instance)
        mock_rental_instance.save.assert_called_once()
        mock_customer_get.assert_called_with(pk=1)
        mock_inventory_qs.return_value.get.assert_called_with(pk=1)
        mock_staff_get.assert_called_with(pk=1)

    @patch("apps.operation.services.transaction.atomic")
    @patch("apps.operation.services.Customer.objects.get")
    def test_create_rental_customer_not_found(self, mock_customer_get, mock_atomic):
        mock_atomic.return_value.__enter__.return_value = None
        mock_customer_get.side_effect = Customer.DoesNotExist

        with self.assertRaises(ValidationError) as cm:
            RentalService.create_rental(999, 1, 1)

        self.assertIn("Customer with ID 999 does not exist", str(cm.exception))

    @patch("apps.operation.services.transaction.atomic")
    @patch("apps.operation.services.Customer.objects.get")
    def test_create_rental_customer_inactive(self, mock_customer_get, mock_atomic):
        mock_atomic.return_value.__enter__.return_value = None
        self.customer_mock.activebool = False
        mock_customer_get.return_value = self.customer_mock

        with self.assertRaises(ValidationError) as cm:
            RentalService.create_rental(1, 1, 1)

        self.assertIn("Customer is not active", str(cm.exception))

    @patch("apps.operation.services.transaction.atomic")
    @patch("apps.operation.services.Customer.objects.get")
    @patch("apps.operation.services.Inventory.objects.select_for_update")
    @patch("apps.operation.services.Rental.objects.filter")
    def test_create_rental_inventory_rented(
        self, mock_rental_filter, mock_inventory_qs, mock_customer_get, mock_atomic
    ):
        mock_atomic.return_value.__enter__.return_value = None
        mock_customer_get.return_value = self.customer_mock
        mock_inventory_qs.return_value.get.return_value = self.inventory_mock

        # Simulate inventory is rented
        mock_rental_filter.return_value.exists.return_value = True

        with self.assertRaises(ValidationError) as cm:
            RentalService.create_rental(1, 1, 1)

        self.assertIn("currently rented out", str(cm.exception))

    @patch("apps.operation.services.Rental.objects.get")
    def test_return_rental_success(self, mock_rental_get):
        mock_rental_instance = MagicMock()
        mock_rental_instance.return_date = None
        mock_rental_get.return_value = mock_rental_instance

        result = RentalService.return_rental(1)

        self.assertEqual(result, mock_rental_instance)
        self.assertIsNotNone(mock_rental_instance.return_date)
        mock_rental_instance.save.assert_called_once()

    @patch("apps.operation.services.Rental.objects.get")
    def test_return_rental_already_returned(self, mock_rental_get):
        mock_rental_instance = MagicMock()
        mock_rental_instance.return_date = "2023-01-01"
        mock_rental_get.return_value = mock_rental_instance

        with self.assertRaises(ValidationError) as cm:
            RentalService.return_rental(1)

        self.assertIn("already been returned", str(cm.exception))


class RentalViewSetTests(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        # Since we are using GenericViewSet, we need to bind actions manually for testing
        self.create_view = RentalViewSet.as_view({"post": "create"})
        self.return_view = RentalViewSet.as_view({"post": "return_movie"})

    @patch("apps.operation.views.RentalService.create_rental")
    def test_create_action_success(self, mock_service):
        # Mock Serializer Class on the ViewSet
        mock_serializer_cls = MagicMock()

        # Setup Serializer instance
        mock_serializer_instance = mock_serializer_cls.return_value
        mock_serializer_instance.is_valid.return_value = True

        # Mock validated data objects
        mock_customer = MagicMock()
        mock_customer.customer_id = 10
        mock_inventory = MagicMock()
        mock_inventory.inventory_id = 20
        mock_staff = MagicMock()
        mock_staff.staff_id = 30

        mock_serializer_instance.validated_data = {
            "customer": mock_customer,
            "inventory": mock_inventory,
            "staff": mock_staff,
        }

        # Setup Service response
        mock_rental = MagicMock()
        mock_service.return_value = mock_rental

        # Setup Output Serializer data
        mock_serializer_instance.data = {"rental_id": 1, "status": "created"}

        # Patch the serializer_class on RentalViewSet
        with patch.object(RentalViewSet, "serializer_class", mock_serializer_cls):
            # Request
            request = self.factory.post(
                "/api/rentals/", {"customer": 10, "inventory": 20, "staff": 30}
            )
            response = self.create_view(request)

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        mock_service.assert_called_with(customer_id=10, inventory_id=20, staff_id=30)

    @patch("apps.operation.views.RentalService.create_rental")
    def test_create_action_validation_error(self, mock_service):
        # Mock Serializer Class
        mock_serializer_cls = MagicMock()
        mock_serializer_instance = mock_serializer_cls.return_value
        mock_serializer_instance.is_valid.return_value = True

        mock_customer = MagicMock()
        mock_customer.customer_id = 10
        mock_inventory = MagicMock()
        mock_inventory.inventory_id = 20
        mock_staff = MagicMock()
        mock_staff.staff_id = 30

        mock_serializer_instance.validated_data = {
            "customer": mock_customer,
            "inventory": mock_inventory,
            "staff": mock_staff,
        }

        # Setup Service to raise ValidationError
        mock_service.side_effect = ValidationError({"inventory_id": ["Item rented"]})

        with patch.object(RentalViewSet, "serializer_class", mock_serializer_cls):
            # Request
            request = self.factory.post(
                "/api/rentals/", {"customer": 10, "inventory": 20, "staff": 30}
            )
            response = self.create_view(request)

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("inventory_id", response.data)

    @patch("apps.operation.views.RentalService.return_rental")
    def test_return_movie_action_success(self, mock_service):
        # Mock Serializer Class
        mock_serializer_cls = MagicMock()
        mock_serializer_instance = mock_serializer_cls.return_value
        mock_serializer_instance.data = {"rental_id": 1, "return_date": "now"}

        # Setup Service
        mock_rental = MagicMock()
        mock_service.return_value = mock_rental

        with patch.object(RentalViewSet, "serializer_class", mock_serializer_cls):
            # Request
            request = self.factory.post("/api/rentals/1/return_movie/")
            # Note: pk passed to view is usually string from URL if using SimpleRouter,
            # but here we call view directly. DRF view dispatching usually passes args/kwargs.
            response = self.return_view(request, pk=1)

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # The view receives pk=1 (int) because we passed it as kwarg to the view callable.
        mock_service.assert_called_with(1)

    @patch("apps.operation.views.RentalService.return_rental")
    def test_return_movie_action_error(self, mock_service):
        # Setup Service to raise ValidationError
        mock_service.side_effect = ValidationError("Already returned")

        # Request
        request = self.factory.post("/api/rentals/1/return_movie/")
        response = self.return_view(request, pk=1)

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data[0], "Already returned")


class SerializerTests(TestCase):
    def test_inventory_serializer(self):
        # Mock Inventory with related Film and Store
        inventory = MagicMock(spec=Inventory)
        inventory.inventory_id = 1
        inventory.last_update = "2023-01-01"

        # Mock related objects
        inventory.film.title = "Test Film"
        inventory.store.store_id = 100

        serializer = InventorySerializer(inventory)
        data = serializer.data

        self.assertEqual(data["inventory_id"], 1)
        self.assertEqual(data["film_title"], "Test Film")
        self.assertEqual(data["store_id"], 100)

    def test_rental_serializer(self):
        # Mock Rental with related objects
        rental = MagicMock(spec=Rental)
        rental.rental_id = 1
        rental.rental_date = "2023-01-01T10:00:00Z"
        rental.return_date = None

        # Related Inventory -> Film
        rental.inventory.film.title = "The Matrix"

        # Related Customer
        rental.customer.first_name = "John"
        rental.customer.last_name = "Doe"

        # Related Staff
        rental.staff.first_name = "Jane"
        rental.staff.last_name = "Smith"

        serializer = RentalSerializer(rental)
        data = serializer.data

        self.assertEqual(data["rental_id"], 1)
        self.assertEqual(data["film_title"], "The Matrix")
        self.assertEqual(data["customer_name"], "John Doe")
        self.assertEqual(data["staff_name"], "Jane Smith")
        self.assertEqual(data["is_returned"], False)

        # Test returned case
        rental.return_date = "2023-01-02T10:00:00Z"
        serializer = RentalSerializer(rental)
        self.assertEqual(serializer.data["is_returned"], True)

    def test_payment_serializer(self):
        data = {
            "customer_id": 1,
            "staff_id": 2,
            "rental_id": 3,
            "amount": "10.50",
            "payment_date": "2023-01-01T12:00:00Z",
        }
        serializer = PaymentSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(float(serializer.validated_data["amount"]), 10.50)
