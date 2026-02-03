from django.contrib import admin

from .models import Customer, Staff, Users


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = (
        "customer_id",
        "first_name",
        "last_name",
        "email",
        "activebool",
        "create_date",
        "active",
    )
    search_fields = ("first_name", "last_name", "email")
    list_filter = ("activebool", "active", "store")


@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = (
        "staff_id",
        "first_name",
        "last_name",
        "email",
        "username",
        "active",
        "last_update",
    )
    search_fields = ("first_name", "last_name", "email", "username")
    list_filter = ("active", "store")


@admin.register(Users)
class UsersAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "created_at", "updated_at")
    search_fields = ("name", "email")
