from django.contrib import admin

from .models import User, Stock, Portfolio, Holding

class StockAdmin(admin.ModelAdmin):
    list_display = ['id','symbol', 'name']
    list_filter = ['symbol', 'name']
    search_fields = ['symbol', 'name']

class HoldingAdmin(admin.ModelAdmin):
    list_display = ['id', 'stock', 'portfolio']
    list_filter = ['stock', 'portfolio']
    search_fields = ['stock', 'portfolio']

class HoldingInlineAdmin(admin.TabularInline):
    model = Holding

class PortfolioAdmin(admin.ModelAdmin):
    list_display = ['id', 'user']
    list_filter = ['id', 'user']
    search_fields = ['id', 'user']
    inlines = [HoldingInlineAdmin]


# Register your models here.

admin.site.register(Stock, StockAdmin)
admin.site.register(Holding, HoldingAdmin)
admin.site.register(Portfolio, PortfolioAdmin)
admin.site.register(User)