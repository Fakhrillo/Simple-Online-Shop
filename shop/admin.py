from django.contrib import admin
from shop.models import Category, Product
from parler.admin import TranslatableAdmin  
# Register your models here.

@admin.register(Category)
class CategoryAdmin(TranslatableAdmin):
    list_display = ['id', 'name', 'slug']
    list_display_links = list_display

    def get_prepopulated_fields(self, request, obj=None):
        return {'slug': ('name',)}


@admin.register(Product)
class ProductAdmin(TranslatableAdmin):
    list_display = ['id', 'name', 'slug', 'price', 'available', 'created', 'updated']
    list_display_links = ['id', 'name', 'slug']
    list_filter = ['available', 'created', 'updated', 'category']
    list_editable = ['price', 'available']
    
    def get_prepopulated_fields(self, request, obj=None):
        return {'slug': ('name',)}