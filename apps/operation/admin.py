from django.contrib import admin

from .models import Inventory, Payment, Rental


@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = ("inventory_id", "film", "store", "last_update")
    list_filter = ("store", "last_update")
    search_fields = ("film__title",)


@admin.register(Rental)
class RentalAdmin(admin.ModelAdmin):
    list_display = (
        "rental_id",
        "rental_date",
        "inventory",
        "customer",
        "return_date",
        "staff",
        "last_update",
    )
    list_filter = ("rental_date", "return_date", "staff")
    search_fields = ("customer__first_name", "customer__last_name")


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = (
        "payment_id",
        "customer_id",
        "staff_id",
        "rental_id",
        "amount",
        "payment_date",
    )
    list_filter = ("payment_date",)
    search_fields = ("customer_id", "staff_id", "rental_id")
