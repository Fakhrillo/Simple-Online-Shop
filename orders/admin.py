from django.contrib import admin
from orders.models import Order, OrderItem
from django_daisy.mixins import NavTabMixin
# Register your models here.

class OrderItemInline(admin.TabularInline, NavTabMixin):
    model = OrderItem
    raw_id_fields = ['product']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'email', 'address', 'postal_code', 'city', 'paid', 'created', 'updated']
    list_display_links = list_display
    list_filter = ['paid', 'created', 'updated']
    inlines = [OrderItemInline]