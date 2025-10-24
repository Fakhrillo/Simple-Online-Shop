from django.contrib import admin
from orders.models import Order, OrderItem
from django_daisy.mixins import NavTabMixin
from django.utils.safestring import mark_safe
from orders.custom_actions import export_to_csv
# Register your models here.

def order_payment(obj):
    url = obj.get_stripe_url()
    if obj.stripe_id:
        html = f'<a href="{url}" target="_blank">{obj.stripe_id}</a>'
        return mark_safe(html)
    return ''

order_payment.short_description = 'Stripe payment'

class OrderItemInline(admin.TabularInline, NavTabMixin):
    model = OrderItem
    raw_id_fields = ['product']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'email', 'address', 'postal_code', 'city', 'paid', order_payment, 'created', 'updated']
    list_display_links = ['id', 'first_name', 'last_name']
    list_filter = ['paid', 'created', 'updated']
    inlines = [OrderItemInline]
    actions = [export_to_csv]