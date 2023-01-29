from django.contrib import admin
from category.models import Category
# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('category_name','slug','cat_image','updated','created')
    prepopulated_fields = {'slug':('category_name',)}
