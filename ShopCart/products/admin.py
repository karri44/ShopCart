from django.contrib import admin
from .models import Product,Category
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name','category','price','stock','active','featured']
    list_filter = ['category','active','featured']
    search_fields = ['name','brand']
    prepopulated_fields = {'slug':('name',)}
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}
