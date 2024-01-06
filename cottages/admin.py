from django.contrib import admin

from cottages.models import Cottage, CottageComment, CottageImage


@admin.register(Cottage)
class CottageAdmin(admin.ModelAdmin):
    list_display = ("owner", "address", "latitude", "longitude", "options")
    list_display_links = ("owner", "address")


@admin.register(CottageImage)
class CottageImageAdmin(admin.ModelAdmin):
    list_display = ("cottage", )
    list_display_links = ("cottage", )


@admin.register(CottageComment)
class CottageCommentAdmin(admin.ModelAdmin):
    list_display = ("cottage", "comment")
    list_display_links = ("cottage", "comment")
