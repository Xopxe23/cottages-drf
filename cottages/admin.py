from django.contrib import admin
from ordered_model.admin import OrderedModelAdmin

from cottages.models import Cottage, CottageCategory, CottageImage


@admin.register(Cottage)
class CottageAdmin(admin.ModelAdmin):
    list_display = ("id", "town", "name", "price", "guests")
    list_display_links = ("town", "name")


@admin.register(CottageCategory)
class CottageCategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", )
    list_display_links = ("id", "name", )


@admin.register(CottageImage)
class CottageImageAdmin(OrderedModelAdmin):
    list_display = ("id", 'image', 'move_up_down_links', "order")
    list_display_links = ("id", "image")
