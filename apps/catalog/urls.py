from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import ActorViewSet, CategoryViewSet, FilmViewSet, LanguageViewSet

router = DefaultRouter()
router.register(r"languages", LanguageViewSet, basename="language")
router.register(r"categories", CategoryViewSet, basename="category")
router.register(r"actors", ActorViewSet, basename="actor")
router.register(r"films", FilmViewSet, basename="film")

urlpatterns = [
    path("", include(router.urls)),
]
