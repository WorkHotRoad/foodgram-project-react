from django.contrib import admin

from users.models import User
from recipe.models import Tag
from recipe.models import Ingredients
from recipe.models import Recipe


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        "author",
        "name",
        "text",
        "cooking_time",
        "image",
        'ingredients',
        'tags'
    )

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "username",
        "email",
        "first_name",
        "last_name",
        "password"
    )
    list_editable = ("password",)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "color",
        "slug",
    )
    list_editable = ("name", "color", "slug",)


@admin.register(Ingredients)
class IngredientsAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "measurement_unit",
    )
    list_editable = ("name", "measurement_unit",)
