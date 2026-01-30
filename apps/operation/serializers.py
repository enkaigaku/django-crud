from rest_framework import serializers

from .models import Inventory, Payment, Rental


class InventorySerializer(serializers.ModelSerializer):
    """Serializer for Inventory model"""

    film_title = serializers.CharField(source="film.title", read_only=True)
    store_id = serializers.IntegerField(source="store.store_id", read_only=True)

    class Meta:
        model = Inventory
        fields = [
            "inventory_id",
            "film",
            "film_title",
            "store",
            "store_id",
            "last_update",
        ]
        read_only_fields = ["inventory_id", "last_update"]


class RentalSerializer(serializers.ModelSerializer):
    """Serializer for Rental model"""

    customer_name = serializers.SerializerMethodField()
    film_title = serializers.CharField(source="inventory.film.title", read_only=True)
    staff_name = serializers.SerializerMethodField()
    is_returned = serializers.SerializerMethodField()

    class Meta:
        model = Rental
        fields = [
            "rental_id",
            "rental_date",
            "inventory",
            "film_title",
            "customer",
            "customer_name",
            "return_date",
            "is_returned",
            "staff",
            "staff_name",
            "last_update",
        ]
        read_only_fields = ["rental_id", "last_update"]

    def get_customer_name(self, obj):
        """Get customer full name"""
        return f"{obj.customer.first_name} {obj.customer.last_name}".strip()

    def get_staff_name(self, obj):
        """Get staff full name"""
        return f"{obj.staff.first_name} {obj.staff.last_name}".strip()

    def get_is_returned(self, obj):
        """Check if rental is returned"""
        return obj.return_date is not None


class PaymentSerializer(serializers.ModelSerializer):
    """Serializer for Payment model"""

    class Meta:
        model = Payment
        fields = [
            "payment_id",
            "customer_id",
            "staff_id",
            "rental_id",
            "amount",
            "payment_date",
        ]
        read_only_fields = ["payment_id"]
