"""
Django REST Framework ViewSets for DVD Rental API
"""
from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from .models import Language, Category, Country, City, Actor, Film, Address, Store, Staff
from .serializers import (
    LanguageSerializer, CategorySerializer, CountrySerializer, CitySerializer,
    ActorSerializer, FilmSerializer, AddressSerializer, StoreSerializer, StaffSerializer
)


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


class ActorViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Actor model.

    Provides CRUD operations for actor data with search by name.
    """
    queryset = Actor.objects.all()
    serializer_class = ActorSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['first_name', 'last_name']
    ordering_fields = ['actor_id', 'first_name', 'last_name']
    ordering = ['last_name', 'first_name']


class FilmViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Film model.

    Provides CRUD operations for film data with search, filter, and ordering.
    Optimized with select_related for language relationships.
    """
    queryset = Film.objects.select_related('language', 'original_language').all()
    serializer_class = FilmSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['rating', 'release_year', 'language']
    search_fields = ['title', 'description']
    ordering_fields = ['film_id', 'title', 'release_year', 'rental_rate']
    ordering = ['title']


class AddressViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Address model.

    Provides CRUD operations for address data with city and country information.
    """
    queryset = Address.objects.select_related('city', 'city__country').all()
    serializer_class = AddressSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['city', 'district']
    search_fields = ['address', 'district', 'postal_code', 'phone']
    ordering_fields = ['address_id', 'district']
    ordering = ['address_id']


class StoreViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Store model.

    Provides CRUD operations for store data.
    """
    queryset = Store.objects.select_related('address', 'address__city').all()
    serializer_class = StoreSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    ordering_fields = ['store_id']
    ordering = ['store_id']


class StaffViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Staff model.

    Provides CRUD operations for staff data with name search.
    """
    queryset = Staff.objects.select_related('store', 'address').all()
    serializer_class = StaffSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['store', 'active']
    search_fields = ['first_name', 'last_name', 'email', 'username']
    ordering_fields = ['staff_id', 'first_name', 'last_name']
    ordering = ['staff_id']
