from django.contrib import admin
from .models import Product
# Register your models here.

@admin.register(Product)

class NameAdmin(admin.ModelAdmin):
    list_display = ('product_name','price','stock','category','modified','is_available')
    prepopulated_fields = {'slug':('product_name',)}
