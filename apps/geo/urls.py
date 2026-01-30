from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import AddressViewSet, CityViewSet, CountryViewSet, StoreViewSet

router = DefaultRouter()
router.register(r"countries", CountryViewSet, basename="country")
router.register(r"cities", CityViewSet, basename="city")
router.register(r"addresses", AddressViewSet, basename="address")
router.register(r"stores", StoreViewSet, basename="store")

urlpatterns = [
    path("", include(router.urls)),
]
