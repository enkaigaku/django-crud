from rest_framework import serializers

from .models import Customer, Staff


class StaffSerializer(serializers.ModelSerializer):
    """Serializer for Staff model"""

    full_name = serializers.SerializerMethodField()
    store_id = serializers.IntegerField(source="store.store_id", read_only=True)

    class Meta:
        model = Staff
        fields = [
            "staff_id",
            "first_name",
            "last_name",
            "full_name",
            "address",
            "email",
            "store",
            "store_id",
            "active",
            "username",
            "last_update",
        ]
        read_only_fields = ["staff_id", "last_update", "full_name"]
        extra_kwargs = {
            "password": {"write_only": True},
            "password_hash": {"write_only": True},
        }

    def get_full_name(self, obj):
        """Combine first and last name"""
        return f"{obj.first_name} {obj.last_name}".strip()


class CustomerSerializer(serializers.ModelSerializer):
    """Serializer for Customer model"""

    full_name = serializers.SerializerMethodField()
    store_id = serializers.IntegerField(source="store.store_id", read_only=True)
    address_info = serializers.CharField(source="address.address", read_only=True)

    class Meta:
        model = Customer
        fields = [
            "customer_id",
            "store",
            "store_id",
            "first_name",
            "last_name",
            "full_name",
            "email",
            "address",
            "address_info",
            "activebool",
            "create_date",
            "last_update",
            "active",
        ]
        read_only_fields = ["customer_id", "create_date", "last_update", "full_name"]
        extra_kwargs = {
            "password_hash": {"write_only": True},
        }

    def get_full_name(self, obj):
        """Combine first and last name"""
        return f"{obj.first_name} {obj.last_name}".strip()
