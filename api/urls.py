"""
API URL Configuration
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter

# Create a router for automatic URL routing
router = DefaultRouter()

# Register viewsets here
# Example: router.register(r'films', FilmViewSet, basename='film')

urlpatterns = [
    path('', include(router.urls)),
]
