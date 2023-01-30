from django.contrib import admin
from .models import Cart,CartItem
# Register your models here.

@admin.register(Cart)

class CartAdmin(admin.ModelAdmin):
    list_display = ('cart_id','date_added')

@admin.register(CartItem)

class CartAdmin(admin.ModelAdmin):
    list_display = ('product','cart','quantity','is_active')