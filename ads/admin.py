from django.contrib import admin

from ads.models import Category, Ads, User, Location


@admin.register(Ads)
class AdAdmin(admin.ModelAdmin):
    list_display = ("name", "author", "price", "is_published")
    search_fields = ("name", "description")
    list_filter = ("is_published",)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ()


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "first_name", "last_name")
    search_fields = ("username",)
    list_filter = ("role",)


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ()
