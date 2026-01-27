"""
Django REST Framework Serializers for DVD Rental API
"""
from rest_framework import serializers
from .models import Language, Category, Country, City, Actor, Film, Address, Store, Staff


class LanguageSerializer(serializers.ModelSerializer):
    """Serializer for Language model"""

    class Meta:
        model = Language
        fields = ['language_id', 'name', 'last_update']
        read_only_fields = ['language_id', 'last_update']


class CategorySerializer(serializers.ModelSerializer):
    """Serializer for Category model"""

    class Meta:
        model = Category
        fields = ['category_id', 'name', 'last_update']
        read_only_fields = ['category_id', 'last_update']


class CountrySerializer(serializers.ModelSerializer):
    """Serializer for Country model"""

    class Meta:
        model = Country
        fields = ['country_id', 'country', 'last_update']
        read_only_fields = ['country_id', 'last_update']


class CitySerializer(serializers.ModelSerializer):
    """Serializer for City model"""
    country_name = serializers.CharField(source='country.country', read_only=True)

    class Meta:
        model = City
        fields = ['city_id', 'city', 'country', 'country_name', 'last_update']
        read_only_fields = ['city_id', 'last_update']


class ActorSerializer(serializers.ModelSerializer):
    """Serializer for Actor model"""
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = Actor
        fields = ['actor_id', 'first_name', 'last_name', 'full_name', 'last_update']
        read_only_fields = ['actor_id', 'last_update', 'full_name']

    def get_full_name(self, obj):
        """Combine first and last name"""
        return f"{obj.first_name} {obj.last_name}".strip()


class FilmSerializer(serializers.ModelSerializer):
    """Serializer for Film model with basic info"""
    language_name = serializers.CharField(source='language.name', read_only=True)
    original_language_name = serializers.CharField(source='original_language.name', read_only=True)

    class Meta:
        model = Film
        fields = [
            'film_id', 'title', 'description', 'release_year',
            'language', 'language_name', 'original_language', 'original_language_name',
            'rental_duration', 'rental_rate', 'length', 'replacement_cost',
            'rating', 'last_update'
        ]
        read_only_fields = ['film_id', 'last_update']


class AddressSerializer(serializers.ModelSerializer):
    """Serializer for Address model"""
    city_name = serializers.CharField(source='city.city', read_only=True)
    country_name = serializers.CharField(source='city.country.country', read_only=True)

    class Meta:
        model = Address
        fields = [
            'address_id', 'address', 'address2', 'district',
            'city', 'city_name', 'country_name',
            'postal_code', 'phone', 'last_update'
        ]
        read_only_fields = ['address_id', 'last_update']


class StoreSerializer(serializers.ModelSerializer):
    """Serializer for Store model"""
    address_info = AddressSerializer(source='address', read_only=True)

    class Meta:
        model = Store
        fields = ['store_id', 'manager_staff_id', 'address', 'address_info', 'last_update']
        read_only_fields = ['store_id', 'last_update']


class StaffSerializer(serializers.ModelSerializer):
    """Serializer for Staff model"""
    full_name = serializers.SerializerMethodField()
    store_id = serializers.IntegerField(source='store.store_id', read_only=True)

    class Meta:
        model = Staff
        fields = [
            'staff_id', 'first_name', 'last_name', 'full_name',
            'address', 'email', 'store', 'store_id', 'active',
            'username', 'last_update'
        ]
        read_only_fields = ['staff_id', 'last_update', 'full_name']
        extra_kwargs = {
            'password': {'write_only': True},
            'password_hash': {'write_only': True},
        }

    def get_full_name(self, obj):
        """Combine first and last name"""
        return f"{obj.first_name} {obj.last_name}".strip()
