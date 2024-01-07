from django.contrib import admin

from towns.models import AttractionImage, Town, TownAttraction, TownImage


@admin.register(Town)
class TownAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    list_display_links = ("id", "name")


@admin.register(TownImage)
class TownImageAdmin(admin.ModelAdmin):
    list_display = ("id", "town")
    list_display_links = ("id", "town")


@admin.register(TownAttraction)
class TownAttractionAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "town")
    list_display_links = ("id", "name")


@admin.register(AttractionImage)
class AttractionImageAdmin(admin.ModelAdmin):
    list_display = ("id", "attraction")
    list_display_links = ("id", "attraction")
