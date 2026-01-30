from django.db import models


class Actor(models.Model):
    actor_id = models.AutoField(primary_key=True)
    first_name = models.TextField()
    last_name = models.TextField()
    last_update = models.DateTimeField()

    class Meta:
        managed = False
        db_table = "actor"


class Category(models.Model):
    category_id = models.AutoField(primary_key=True)
    name = models.TextField()
    last_update = models.DateTimeField()

    class Meta:
        managed = False
        db_table = "category"


class Language(models.Model):
    language_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)
    last_update = models.DateTimeField()

    class Meta:
        managed = False
        db_table = "language"


class Film(models.Model):
    film_id = models.AutoField(primary_key=True)
    title = models.TextField()
    description = models.TextField(blank=True, null=True)
    release_year = models.IntegerField(blank=True, null=True)
    language = models.ForeignKey("catalog.Language", models.DO_NOTHING)
    original_language = models.ForeignKey(
        "catalog.Language",
        models.DO_NOTHING,
        related_name="film_original_language_set",
        blank=True,
        null=True,
    )
    rental_duration = models.SmallIntegerField()
    rental_rate = models.DecimalField(max_digits=4, decimal_places=2)
    length = models.SmallIntegerField(blank=True, null=True)
    replacement_cost = models.DecimalField(max_digits=5, decimal_places=2)
    rating = models.TextField(blank=True, null=True)
    last_update = models.DateTimeField()
    special_features = models.TextField(blank=True, null=True)
    fulltext = models.TextField()

    class Meta:
        managed = False
        db_table = "film"


class FilmActor(models.Model):
    pk = models.CompositePrimaryKey("actor_id", "film_id")
    actor = models.ForeignKey("catalog.Actor", models.DO_NOTHING)
    film = models.ForeignKey("catalog.Film", models.DO_NOTHING)
    last_update = models.DateTimeField()

    class Meta:
        managed = False
        db_table = "film_actor"


class FilmCategory(models.Model):
    pk = models.CompositePrimaryKey("film_id", "category_id")
    film = models.ForeignKey("catalog.Film", models.DO_NOTHING)
    category = models.ForeignKey("catalog.Category", models.DO_NOTHING)
    last_update = models.DateTimeField()

    class Meta:
        managed = False
        db_table = "film_category"
