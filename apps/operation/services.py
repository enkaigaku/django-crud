from django.core.exceptions import ValidationError
from django.db import transaction
from django.utils import timezone

from apps.account.models import Customer, Staff

from .models import Inventory, Rental


class RentalService:
    """
    Service layer for Rental business logic.
    Encapsulates complex operations like inventory checking and return processing.
    """

    @staticmethod
    def create_rental(customer_id, inventory_id, staff_id):
        """
        Create a new rental record with business logic validation.

        Args:
            customer_id (int): ID of the customer renting the item.
            inventory_id (int): ID of the inventory item being rented.
            staff_id (int): ID of the staff member processing the rental.

        Returns:
            Rental: The created rental instance.

        Raises:
            ValidationError: If customer/inventory invalid or item not available.
        """
        with transaction.atomic():
            # 1. Validate Customer
            try:
                customer = Customer.objects.get(pk=customer_id)
            except Customer.DoesNotExist:
                raise ValidationError(
                    {"customer_id": f"Customer with ID {customer_id} does not exist."}
                )

            # Check if customer is active (using activebool based on schema)
            if not customer.activebool:
                raise ValidationError(
                    {"customer_id": "Customer is not active and cannot rent items."}
                )

            # 2. Validate Inventory with Row Lock
            # Use select_for_update() to lock the inventory row until transaction ends.
            # This prevents race conditions where two transactions check availability simultaneously.
            try:
                inventory = Inventory.objects.select_for_update().get(pk=inventory_id)
            except Inventory.DoesNotExist:
                raise ValidationError(
                    {
                        "inventory_id": f"Inventory item with ID {inventory_id} does not exist."
                    }
                )

            # 3. Check availability: Is this inventory item currently rented out?
            # A rental is considered 'open' if return_date is NULL.
            is_rented = Rental.objects.filter(
                inventory=inventory, return_date__isnull=True
            ).exists()

            if is_rented:
                raise ValidationError(
                    {"inventory_id": "This inventory item is currently rented out."}
                )

            # 4. Validate Staff
            try:
                staff = Staff.objects.get(pk=staff_id)
            except Staff.DoesNotExist:
                raise ValidationError(
                    {"staff_id": f"Staff with ID {staff_id} does not exist."}
                )

            # 5. Create Rental
            # We need to handle timestamps manually because managed=False might affect auto_now behavior
            # and we want precise control over rental_date.
            now = timezone.now()

            rental = Rental(
                rental_date=now,
                inventory=inventory,
                customer=customer,
                staff=staff,
                last_update=now,
            )
            rental.save()
            return rental

    @staticmethod
    def return_rental(rental_id):
        """
        Process the return of a rental.

        Args:
            rental_id (int): ID of the rental to return.

        Returns:
            Rental: The updated rental instance.

        Raises:
            ValidationError: If rental not found or already returned.
        """
        try:
            rental = Rental.objects.get(pk=rental_id)
        except Rental.DoesNotExist:
            raise ValidationError(f"Rental with ID {rental_id} does not exist.")

        if rental.return_date is not None:
            raise ValidationError("This rental has already been returned.")

        now = timezone.now()
        rental.return_date = now
        rental.last_update = now
        rental.save()

        return rental
