"""
Django REST Framework Serializers for DVD Rental API
"""
from rest_framework import serializers
from .models import Language, Category, Country, City


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
