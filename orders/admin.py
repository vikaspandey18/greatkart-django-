from django.contrib import admin
from orders.models import Payment,Order,OrderProduct
# Register your models here.
@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('user','payment_id','payment_method','amount_paid','status','created_at')
    

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user','payment','order_number','first_name','last_name','status','created_at')


@admin.register(OrderProduct)
class OrderProductAdmin(admin.ModelAdmin):
    list_display = ('order','payment','user','product','product_price','created_at','updated_at')