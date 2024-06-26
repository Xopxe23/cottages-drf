from django.contrib import admin

from .models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'rent', 'ukassa_id', 'amount', 'status', 'created_at')
    list_display_links = ('id', 'rent')
    search_fields = ('id', 'rent__id', 'ukassa_id', 'status')
    list_filter = ('status', 'created_at')
