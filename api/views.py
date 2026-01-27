"""
Django REST Framework ViewSets for DVD Rental API
"""
from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from .models import Language, Category, Country, City
from .serializers import LanguageSerializer, CategorySerializer, CountrySerializer, CitySerializer


class LanguageViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Language model.

    Provides CRUD operations for language data.
    """
    queryset = Language.objects.all()
    serializer_class = LanguageSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['language_id', 'name']
    ordering = ['name']


class CategoryViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Category model.

    Provides CRUD operations for film category data.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['category_id', 'name']
    ordering = ['name']


class CountryViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Country model.

    Provides CRUD operations for country data.
    """
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['country']
    ordering_fields = ['country_id', 'country']
    ordering = ['country']


class CityViewSet(viewsets.ModelViewSet):
    """
    ViewSet for City model.

    Provides CRUD operations for city data with country relationship.
    """
    queryset = City.objects.select_related('country').all()
    serializer_class = CitySerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['country']
    search_fields = ['city', 'country__country']
    ordering_fields = ['city_id', 'city']
    ordering = ['city']
