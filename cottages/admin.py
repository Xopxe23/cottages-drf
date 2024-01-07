from django.contrib import admin

from cottages.models import Cottage, CottageAmenities, CottageCategory, CottageImage, CottageRules


@admin.register(Cottage)
class CottageAdmin(admin.ModelAdmin):
    list_display = ("town", "name", "price", "guests")
    list_display_links = ("town", "name")


@admin.register(CottageCategory)
class CottageCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", )
    list_display_links = ("name", )


@admin.register(CottageImage)
class CottageImageAdmin(admin.ModelAdmin):
    list_display = ("cottage", )
    list_display_links = ("cottage", )


@admin.register(CottageRules)
class CottageRulesAdmin(admin.ModelAdmin):
    list_display = ("cottage", "check_in_time", "check_out_time", "need_documents")
    list_display_links = ("cottage", )


@admin.register(CottageAmenities)
class CottageAmenitiesAdmin(admin.ModelAdmin):
    list_display = ("cottage", "parking_spaces", "wifi", "tv")
    list_display_links = ("cottage", )
