from django.db import models


class Country(models.Model):
    country_id = models.AutoField(primary_key=True)
    country = models.TextField()
    last_update = models.DateTimeField()

    class Meta:
        managed = False
        db_table = "country"


class City(models.Model):
    city_id = models.AutoField(primary_key=True)
    city = models.TextField()
    country = models.ForeignKey("geo.Country", models.DO_NOTHING)
    last_update = models.DateTimeField()

    class Meta:
        managed = False
        db_table = "city"


class Address(models.Model):
    address_id = models.AutoField(primary_key=True)
    address = models.TextField()
    address2 = models.TextField(blank=True, null=True)
    district = models.TextField()
    city = models.ForeignKey("geo.City", models.DO_NOTHING)
    postal_code = models.TextField(blank=True, null=True)
    phone = models.TextField()
    last_update = models.DateTimeField()

    class Meta:
        managed = False
        db_table = "address"


class Store(models.Model):
    store_id = models.AutoField(primary_key=True)
    manager_staff_id = models.IntegerField(unique=True)
    address = models.ForeignKey("geo.Address", models.DO_NOTHING)
    last_update = models.DateTimeField()

    class Meta:
        managed = False
        db_table = "store"
