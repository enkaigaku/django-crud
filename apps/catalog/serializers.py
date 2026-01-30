from rest_framework import serializers

from .models import Actor, Category, Film, Language


class LanguageSerializer(serializers.ModelSerializer):
    """Serializer for Language model"""

    class Meta:
        model = Language
        fields = ["language_id", "name", "last_update"]
        read_only_fields = ["language_id", "last_update"]


class CategorySerializer(serializers.ModelSerializer):
    """Serializer for Category model"""

    class Meta:
        model = Category
        fields = ["category_id", "name", "last_update"]
        read_only_fields = ["category_id", "last_update"]


class ActorSerializer(serializers.ModelSerializer):
    """Serializer for Actor model"""

    full_name = serializers.SerializerMethodField()

    class Meta:
        model = Actor
        fields = ["actor_id", "first_name", "last_name", "full_name", "last_update"]
        read_only_fields = ["actor_id", "last_update", "full_name"]

    def get_full_name(self, obj):
        """Combine first and last name"""
        return f"{obj.first_name} {obj.last_name}".strip()


class FilmSerializer(serializers.ModelSerializer):
    """Serializer for Film model with basic info"""

    language_name = serializers.CharField(source="language.name", read_only=True)
    original_language_name = serializers.CharField(
        source="original_language.name", read_only=True
    )

    class Meta:
        model = Film
        fields = [
            "film_id",
            "title",
            "description",
            "release_year",
            "language",
            "language_name",
            "original_language",
            "original_language_name",
            "rental_duration",
            "rental_rate",
            "length",
            "replacement_cost",
            "rating",
            "last_update",
        ]
        read_only_fields = ["film_id", "last_update"]
