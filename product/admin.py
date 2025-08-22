from django.contrib import admin
from .models import HalfProduct


@admin.register(HalfProduct)
class HalfProductAdmin(admin.ModelAdmin):
    list_display = ("name", "type", "price", "total_kg", "total_price", "amount_of_qop", "kg", "barn")
    search_fields = ("name",)
    list_filter = ("type", "barn")

    def get_readonly_fields(self, request, obj=None):
        """
        Agar type == 'kg' bo'lsa, faqat amount_of_qop readonly bo'ladi.
        """
        if obj and obj.type == "kg":
            return ("amount_of_qop",)
        return super().get_readonly_fields(request, obj)

    def save_model(self, request, obj, form, change):
        """
        Admin paneldan saqlashda total_kg va total_price avtomatik hisoblanadi
        """
        if obj.type == "kg":
            obj.total_kg = obj.kg or 0
            obj.amount_of_qop = None
        elif obj.type == "qop":
            obj.total_kg = (obj.amount_of_qop or 0) * (obj.kg or 0)
        else:
            obj.total_kg = 0

        obj.total_price = (obj.price or 0) * obj.total_kg
        super().save_model(request, obj, form, change)


from django.contrib import admin
from .models import Product, HalfProduct, ProductHalfProduct


class ProductHalfProductInline(admin.TabularInline):
    """Product ichida HalfProductlarni ko‘rsatish va boshqarish"""
    model = ProductHalfProduct
    extra = 1
    autocomplete_fields = ["half_product"]
    fields = ("half_product", "used_kg")
    readonly_fields = ()

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        obj.product.update_totals()

    def delete_model(self, request, obj):
        product = obj.product
        super().delete_model(request, obj)
        product.update_totals()


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "type", "total_kg", "total_price", "created_at")
    search_fields = ("name",)
    list_filter = ("type", "created_at")
    inlines = [ProductHalfProductInline]



@admin.register(ProductHalfProduct)
class ProductHalfProductAdmin(admin.ModelAdmin):
    list_display = ("product", "half_product", "used_kg","created_at")
    list_filter = ("half_product__type", "product__type")
    search_fields = ("product__name", "half_product__name")