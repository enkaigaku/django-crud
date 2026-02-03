from django.contrib import admin

from .models import Address, City, Country, Store


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ("country_id", "country", "last_update")
    search_fields = ("country",)


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ("city_id", "city", "country", "last_update")
    search_fields = ("city",)
    list_filter = ("country",)


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = (
        "address_id",
        "address",
        "district",
        "city",
        "phone",
        "last_update",
    )
    search_fields = ("address", "district", "phone")
    list_filter = ("city",)


@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ("store_id", "manager_staff_id", "address", "last_update")
    search_fields = ("manager_staff_id",)
