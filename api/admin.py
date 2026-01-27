from django.contrib import admin
from .models import (
    Actor, Address, Category, City, Country, Customer, Film, FilmActor,
    FilmCategory, Inventory, Language, Payment, Rental, Staff, Store
)


# ============================================================================
# Phase 1: 基础模型配置
# ============================================================================

@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    """语言管理"""
    list_display = ['language_id', 'name', 'last_update']
    search_fields = ['name']
    ordering = ['name']
    readonly_fields = ['last_update']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """电影分类管理"""
    list_display = ['category_id', 'name', 'last_update']
    search_fields = ['name']
    ordering = ['name']
    readonly_fields = ['last_update']


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    """国家管理"""
    list_display = ['country_id', 'country', 'last_update']
    search_fields = ['country']
    ordering = ['country']
    readonly_fields = ['last_update']


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    """城市管理"""
    list_display = ['city_id', 'city', 'get_country_name', 'last_update']
    search_fields = ['city']
    list_filter = ['country']
    ordering = ['city']
    readonly_fields = ['last_update']

    def get_queryset(self, request):
        """优化查询性能"""
        qs = super().get_queryset(request)
        return qs.select_related('country')

    @admin.display(description='国家', ordering='country__country')
    def get_country_name(self, obj):
        return obj.country.country


# ============================================================================
# Phase 2: 核心业务模型配置
# ============================================================================

@admin.register(Actor)
class ActorAdmin(admin.ModelAdmin):
    """演员管理"""
    list_display = ['actor_id', 'first_name', 'last_name', 'full_name', 'last_update']
    search_fields = ['first_name', 'last_name']
    ordering = ['last_name', 'first_name']
    readonly_fields = ['last_update']

    @admin.display(description='全名', ordering='last_name')
    def full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}".strip()


# 内联编辑：电影-演员关联
class FilmActorInline(admin.TabularInline):
    """电影演员关联（内联）"""
    model = FilmActor
    extra = 3
    fields = ['actor']
    autocomplete_fields = ['actor']


# 内联编辑：电影-分类关联
class FilmCategoryInline(admin.TabularInline):
    """电影分类关联（内联）"""
    model = FilmCategory
    extra = 2
    fields = ['category']


@admin.register(Film)
class FilmAdmin(admin.ModelAdmin):
    """电影管理"""
    list_display = [
        'film_id', 'title', 'get_language_name', 'rating',
        'release_year', 'rental_rate', 'rental_duration', 'last_update'
    ]
    search_fields = ['title', 'description']
    list_filter = ['rating', 'release_year', 'language']
    ordering = ['title']
    readonly_fields = ['last_update', 'fulltext']
    inlines = [FilmActorInline, FilmCategoryInline]

    fieldsets = (
        ('基本信息', {
            'fields': ('title', 'description', 'release_year', 'language', 'original_language')
        }),
        ('租赁信息', {
            'fields': ('rental_duration', 'rental_rate', 'replacement_cost')
        }),
        ('其他信息', {
            'fields': ('rating', 'length', 'special_features', 'last_update', 'fulltext'),
            'classes': ('collapse',)
        }),
    )

    def get_queryset(self, request):
        """优化查询性能"""
        qs = super().get_queryset(request)
        return qs.select_related('language', 'original_language')

    @admin.display(description='语言', ordering='language__name')
    def get_language_name(self, obj):
        return obj.language.name


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    """地址管理"""
    list_display = [
        'address_id', 'address', 'address2', 'district',
        'get_city_name', 'get_country_name', 'postal_code', 'phone'
    ]
    search_fields = ['address', 'district', 'postal_code', 'phone']
    list_filter = ['city__country']
    ordering = ['address']
    readonly_fields = ['last_update']

    def get_queryset(self, request):
        """优化查询性能"""
        qs = super().get_queryset(request)
        return qs.select_related('city__country')

    @admin.display(description='城市', ordering='city__city')
    def get_city_name(self, obj):
        return obj.city.city

    @admin.display(description='国家')
    def get_country_name(self, obj):
        return obj.city.country.country


# ============================================================================
# Phase 3: 支持性模型配置
# ============================================================================

@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    """门店管理"""
    list_display = ['store_id', 'manager_staff_id', 'get_address_info', 'last_update']
    search_fields = ['address__address', 'address__district']
    readonly_fields = ['last_update']

    def get_queryset(self, request):
        """优化查询性能"""
        qs = super().get_queryset(request)
        return qs.select_related('address__city__country')

    @admin.display(description='地址信息')
    def get_address_info(self, obj):
        return f"{obj.address.address}, {obj.address.city.city}, {obj.address.city.country.country}"


@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    """员工管理"""
    list_display = [
        'staff_id', 'full_name', 'email', 'username',
        'get_store_id', 'active', 'last_update'
    ]
    search_fields = ['first_name', 'last_name', 'email', 'username']
    list_filter = ['active', 'store']
    ordering = ['last_name', 'first_name']
    readonly_fields = ['last_update']

    fieldsets = (
        ('基本信息', {
            'fields': ('first_name', 'last_name', 'email', 'username')
        }),
        ('工作信息', {
            'fields': ('store', 'address', 'active')
        }),
        ('系统信息', {
            'fields': ('password_hash', 'last_update'),
            'classes': ('collapse',)
        }),
    )

    def get_queryset(self, request):
        """优化查询性能"""
        qs = super().get_queryset(request)
        return qs.select_related('address', 'store')

    @admin.display(description='全名', ordering='last_name')
    def full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}".strip()

    @admin.display(description='门店', ordering='store__store_id')
    def get_store_id(self, obj):
        return f"门店 #{obj.store.store_id}"


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    """客户管理"""
    list_display = [
        'customer_id', 'full_name', 'email', 'get_store_id',
        'activebool', 'create_date', 'last_update'
    ]
    search_fields = ['first_name', 'last_name', 'email']
    list_filter = ['activebool', 'store', 'create_date']
    date_hierarchy = 'create_date'
    ordering = ['last_name', 'first_name']
    readonly_fields = ['create_date', 'last_update']

    fieldsets = (
        ('基本信息', {
            'fields': ('first_name', 'last_name', 'email')
        }),
        ('业务信息', {
            'fields': ('store', 'address', 'activebool', 'active', 'create_date')
        }),
        ('系统信息', {
            'fields': ('password_hash', 'last_update'),
            'classes': ('collapse',)
        }),
    )

    def get_queryset(self, request):
        """优化查询性能"""
        qs = super().get_queryset(request)
        return qs.select_related('address', 'store')

    @admin.display(description='全名', ordering='last_name')
    def full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}".strip()

    @admin.display(description='门店', ordering='store__store_id')
    def get_store_id(self, obj):
        return f"门店 #{obj.store.store_id}"


# ============================================================================
# Phase 4: 交易模型配置
# ============================================================================

@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    """库存管理"""
    list_display = ['inventory_id', 'get_film_title', 'get_store_id', 'last_update']
    search_fields = ['film__title']
    list_filter = ['store']
    ordering = ['inventory_id']
    readonly_fields = ['last_update']

    def get_queryset(self, request):
        """优化查询性能"""
        qs = super().get_queryset(request)
        return qs.select_related('film', 'store')

    @admin.display(description='电影标题', ordering='film__title')
    def get_film_title(self, obj):
        return obj.film.title

    @admin.display(description='门店', ordering='store__store_id')
    def get_store_id(self, obj):
        return f"门店 #{obj.store.store_id}"


@admin.register(Rental)
class RentalAdmin(admin.ModelAdmin):
    """租赁管理"""
    list_display = [
        'rental_id', 'get_customer_name', 'get_film_title',
        'rental_date', 'return_date', 'is_returned', 'get_staff_name'
    ]
    search_fields = ['customer__first_name', 'customer__last_name', 'inventory__film__title']
    list_filter = ['rental_date', 'return_date', 'staff']
    date_hierarchy = 'rental_date'
    ordering = ['-rental_date']
    readonly_fields = ['last_update']

    def get_queryset(self, request):
        """优化查询性能"""
        qs = super().get_queryset(request)
        return qs.select_related('inventory__film', 'customer', 'staff')

    @admin.display(description='客户名称', ordering='customer__last_name')
    def get_customer_name(self, obj):
        return f"{obj.customer.first_name} {obj.customer.last_name}".strip()

    @admin.display(description='电影标题', ordering='inventory__film__title')
    def get_film_title(self, obj):
        return obj.inventory.film.title

    @admin.display(description='员工名称', ordering='staff__last_name')
    def get_staff_name(self, obj):
        return f"{obj.staff.first_name} {obj.staff.last_name}".strip()

    @admin.display(description='归还状态', boolean=True)
    def is_returned(self, obj):
        return obj.return_date is not None


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    """支付管理"""
    list_display = [
        'payment_id', 'customer_id', 'staff_id',
        'rental_id', 'amount', 'payment_date'
    ]
    search_fields = ['customer_id', 'rental_id']
    list_filter = ['payment_date', 'staff_id']
    date_hierarchy = 'payment_date'
    ordering = ['-payment_date']
    readonly_fields = ['payment_date']


# ============================================================================
# Admin 站点自定义
# ============================================================================

admin.site.site_header = 'DVD 租赁管理系统'
admin.site.site_title = 'DVD 租赁后台'
admin.site.index_title = '欢迎使用 DVD 租赁管理系统'
