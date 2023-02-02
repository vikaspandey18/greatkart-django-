from django.contrib import admin
from .models import Product, Variation
# Register your models here.

@admin.register(Product)
class NameAdmin(admin.ModelAdmin):
    list_display = ('product_name','price','stock','category','modified','is_available')
    prepopulated_fields = {'slug':('product_name',)}
    
    
@admin.register(Variation)
class VariationAdmin(admin.ModelAdmin):
    list_display = ('product','variation_category','variation_value','is_active','created')
    list_editable = ('is_active',)
    list_filter = ('product','variation_category','variation_value')

