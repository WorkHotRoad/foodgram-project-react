from django.contrib import admin

from users.models import User
from .models import Tag


class UserAdmin(admin.ModelAdmin):
    list_display = (
        "username",
        "email",
        "first_name",
        "last_name",
        "password"
    )
    list_editable = ("password",)


class TagAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "color",
        "slug",
    )
    list_editable = ("name", "color", "slug",)


admin.site.register(User, UserAdmin)
admin.site.register(Tag, TagAdmin)