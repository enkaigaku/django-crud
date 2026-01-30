from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import InventoryViewSet, PaymentViewSet, RentalViewSet

router = DefaultRouter()
router.register(r"inventory", InventoryViewSet, basename="inventory")
router.register(r"rentals", RentalViewSet, basename="rental")
router.register(r"payments", PaymentViewSet, basename="payment")

urlpatterns = [
    path("", include(router.urls)),
]
