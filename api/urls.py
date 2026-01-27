"""
API URL Configuration
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LanguageViewSet, CategoryViewSet, CountryViewSet, CityViewSet

# Create a router for automatic URL routing
router = DefaultRouter()

# Register simple CRUD viewsets
router.register(r'languages', LanguageViewSet, basename='language')
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'countries', CountryViewSet, basename='country')
router.register(r'cities', CityViewSet, basename='city')

urlpatterns = [
    path('', include(router.urls)),
]
