from django.contrib import admin

from .models import Actor, Category, Film, Language


@admin.register(Actor)
class ActorAdmin(admin.ModelAdmin):
    list_display = ("actor_id", "first_name", "last_name", "last_update")
    search_fields = ("first_name", "last_name")


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("category_id", "name", "last_update")
    search_fields = ("name",)


@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ("language_id", "name", "last_update")
    search_fields = ("name",)


@admin.register(Film)
class FilmAdmin(admin.ModelAdmin):
    list_display = (
        "film_id",
        "title",
        "release_year",
        "language",
        "rental_rate",
        "rating",
        "last_update",
    )
    search_fields = ("title", "description")
    list_filter = ("release_year", "language", "rating")
