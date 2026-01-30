from django.db import models


class Customer(models.Model):
    customer_id = models.AutoField(primary_key=True)
    store = models.ForeignKey("geo.Store", models.DO_NOTHING)
    first_name = models.TextField()
    last_name = models.TextField()
    email = models.TextField(blank=True, null=True)
    address = models.ForeignKey("geo.Address", models.DO_NOTHING)
    activebool = models.BooleanField()
    create_date = models.DateField()
    last_update = models.DateTimeField(blank=True, null=True)
    active = models.IntegerField(blank=True, null=True)
    password_hash = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "customer"


class Staff(models.Model):
    staff_id = models.AutoField(primary_key=True)
    first_name = models.TextField()
    last_name = models.TextField()
    address = models.ForeignKey("geo.Address", models.DO_NOTHING)
    email = models.TextField(blank=True, null=True)
    store = models.ForeignKey("geo.Store", models.DO_NOTHING)
    active = models.BooleanField()
    username = models.TextField()
    password = models.TextField(blank=True, null=True)
    last_update = models.DateTimeField()
    picture = models.BinaryField(blank=True, null=True)
    password_hash = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "staff"


class Users(models.Model):
    name = models.CharField(max_length=255)
    email = models.CharField(unique=True, max_length=255)
    password = models.CharField(max_length=512)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "users"
