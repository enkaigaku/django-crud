from rest_framework import serializers

from .models import Address, City, Country, Store


class CountrySerializer(serializers.ModelSerializer):
    """Serializer for Country model"""

    class Meta:
        model = Country
        fields = ["country_id", "country", "last_update"]
        read_only_fields = ["country_id", "last_update"]


class CitySerializer(serializers.ModelSerializer):
    """Serializer for City model"""

    country_name = serializers.CharField(source="country.country", read_only=True)

    class Meta:
        model = City
        fields = ["city_id", "city", "country", "country_name", "last_update"]
        read_only_fields = ["city_id", "last_update"]


class AddressSerializer(serializers.ModelSerializer):
    """Serializer for Address model"""

    city_name = serializers.CharField(source="city.city", read_only=True)
    country_name = serializers.CharField(source="city.country.country", read_only=True)

    class Meta:
        model = Address
        fields = [
            "address_id",
            "address",
            "address2",
            "district",
            "city",
            "city_name",
            "country_name",
            "postal_code",
            "phone",
            "last_update",
        ]
        read_only_fields = ["address_id", "last_update"]


class StoreSerializer(serializers.ModelSerializer):
    """Serializer for Store model"""

    address_info = AddressSerializer(source="address", read_only=True)

    class Meta:
        model = Store
        fields = [
            "store_id",
            "manager_staff_id",
            "address",
            "address_info",
            "last_update",
        ]
        read_only_fields = ["store_id", "last_update"]
