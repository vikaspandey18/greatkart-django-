from django.db import models
from category.models import Category
from django.urls import reverse

# Create your models here.

class Product(models.Model):
    product_name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200,unique=True)
    description = models.TextField(blank=True, null=True)
    price = models.IntegerField()
    images =  models.ImageField(upload_to='photos/products',blank=True, null=True)
    stock = models.IntegerField()
    is_available = models.BooleanField(default=True)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    
    def get_absolute_url(self):
        return reverse("product_detail", args=[self.category.slug, self.slug])

        
    def __str__(self):
        return self.product_name
    

