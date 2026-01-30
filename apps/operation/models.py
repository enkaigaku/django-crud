from django.db import models


class Inventory(models.Model):
    inventory_id = models.AutoField(primary_key=True)
    film = models.ForeignKey("catalog.Film", models.DO_NOTHING)
    store = models.ForeignKey("geo.Store", models.DO_NOTHING)
    last_update = models.DateTimeField()

    class Meta:
        managed = False
        db_table = "inventory"


class Rental(models.Model):
    rental_id = models.AutoField(primary_key=True)
    rental_date = models.DateTimeField()
    inventory = models.ForeignKey("operation.Inventory", models.DO_NOTHING)
    customer = models.ForeignKey("account.Customer", models.DO_NOTHING)
    return_date = models.DateTimeField(blank=True, null=True)
    staff = models.ForeignKey("account.Staff", models.DO_NOTHING)
    last_update = models.DateTimeField()

    class Meta:
        managed = False
        db_table = "rental"
        unique_together = (("rental_date", "inventory", "customer"),)


class Payment(models.Model):
    payment_id = models.AutoField(primary_key=True)
    customer_id = models.IntegerField()
    staff_id = models.IntegerField()
    rental_id = models.IntegerField()
    amount = models.DecimalField(max_digits=5, decimal_places=2)
    payment_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = "payment"
