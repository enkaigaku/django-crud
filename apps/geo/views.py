from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.filters import OrderingFilter, SearchFilter

from .models import Address, City, Country, Store
from .serializers import (
    AddressSerializer,
    CitySerializer,
    CountrySerializer,
    StoreSerializer,
)


class CountryViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Country model.

    Provides CRUD operations for country data.
    """

    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ["country"]
    ordering_fields = ["country_id", "country"]
    ordering = ["country"]


class CityViewSet(viewsets.ModelViewSet):
    """
    ViewSet for City model.

    Provides CRUD operations for city data with country relationship.
    """

    queryset = City.objects.select_related("country").all()
    serializer_class = CitySerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["country"]
    search_fields = ["city", "country__country"]
    ordering_fields = ["city_id", "city"]
    ordering = ["city"]


class AddressViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Address model.

    Provides CRUD operations for address data with city and country information.
    """

    queryset = Address.objects.select_related("city", "city__country").all()
    serializer_class = AddressSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["city", "district"]
    search_fields = ["address", "district", "postal_code", "phone"]
    ordering_fields = ["address_id", "district"]
    ordering = ["address_id"]


class StoreViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Store model.

    Provides CRUD operations for store data.
    """

    queryset = Store.objects.select_related("address", "address__city").all()
    serializer_class = StoreSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    ordering_fields = ["store_id"]
    ordering = ["store_id"]
