"""Admin configuration per l'app Pharmacy."""
from django.contrib import admin
from .models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'available', 'requires_prescription', 'updated_at']
    list_filter = ['category', 'available', 'requires_prescription']
    search_fields = ['name', 'description', 'sku']
    list_editable = ['price', 'available']
    ordering = ['name']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Informazioni Prodotto', {
            'fields': ('name', 'description', 'category', 'sku')
        }),
        ('Prezzo e Disponibilità', {
            'fields': ('price', 'available', 'requires_prescription')
        }),
        ('Timestamp', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )
