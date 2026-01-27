"""
API URL Configuration
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    LanguageViewSet, CategoryViewSet, CountryViewSet, CityViewSet,
    ActorViewSet, FilmViewSet
)

# Create a router for automatic URL routing
router = DefaultRouter()

# Register simple CRUD viewsets
router.register(r'languages', LanguageViewSet, basename='language')
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'countries', CountryViewSet, basename='country')
router.register(r'cities', CityViewSet, basename='city')

# Register core business viewsets
router.register(r'actors', ActorViewSet, basename='actor')
router.register(r'films', FilmViewSet, basename='film')

urlpatterns = [
    path('', include(router.urls)),
]
