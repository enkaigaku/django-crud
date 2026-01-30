from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.filters import OrderingFilter, SearchFilter

from .models import Actor, Category, Film, Language
from .serializers import (
    ActorSerializer,
    CategorySerializer,
    FilmSerializer,
    LanguageSerializer,
)


class LanguageViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Language model.

    Provides CRUD operations for language data.
    """

    queryset = Language.objects.all()
    serializer_class = LanguageSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ["name"]
    ordering_fields = ["language_id", "name"]
    ordering = ["name"]


class CategoryViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Category model.

    Provides CRUD operations for film category data.
    """

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ["name"]
    ordering_fields = ["category_id", "name"]
    ordering = ["name"]


class ActorViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Actor model.

    Provides CRUD operations for actor data with search by name.
    """

    queryset = Actor.objects.all()
    serializer_class = ActorSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ["first_name", "last_name"]
    ordering_fields = ["actor_id", "first_name", "last_name"]
    ordering = ["last_name", "first_name"]


class FilmViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Film model.

    Provides CRUD operations for film data with search, filter, and ordering.
    Optimized with select_related for language relationships.
    """

    queryset = Film.objects.select_related("language", "original_language").all()
    serializer_class = FilmSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["rating", "release_year", "language"]
    search_fields = ["title", "description"]
    ordering_fields = ["film_id", "title", "release_year", "rental_rate"]
    ordering = ["title"]
