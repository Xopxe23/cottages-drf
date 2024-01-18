from django.contrib import admin
from ordered_model.admin import OrderedModelAdmin

from cottages.models import Cottage, CottageAmenities, CottageCategory, CottageImage, CottageRules


@admin.register(Cottage)
class CottageAdmin(admin.ModelAdmin):
    list_display = ("town", "name", "price", "guests")
    list_display_links = ("town", "name")


@admin.register(CottageCategory)
class CottageCategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", )
    list_display_links = ("id", "name", )


@admin.register(CottageImage)
class CottageImageAdmin(OrderedModelAdmin):
    list_display = ("id", 'image', 'move_up_down_links', "order")
    list_display_links = ("id", "image")


@admin.register(CottageRules)
class CottageRulesAdmin(admin.ModelAdmin):
    list_display = ("cottage", "check_in_time", "check_out_time", "need_documents")
    list_display_links = ("cottage", )


@admin.register(CottageAmenities)
class CottageAmenitiesAdmin(admin.ModelAdmin):
    list_display = ("cottage", "parking_spaces", "wifi", "tv")
    list_display_links = ("cottage", )
