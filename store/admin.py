from django.contrib import admin
from .models import Region, Attraction


@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Attraction)
class AttractionAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'region', 'ticket_price', 'available', 'created_at')
    list_filter = ('region', 'available', 'category')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}