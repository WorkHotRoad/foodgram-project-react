from django.contrib import admin

from users.models import User
from recipe.models import Tag, Ingredients, Recipe


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




@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "author",
        "name",
        "text",
        "cooking_time",
        "image",
        'get_ingredients',
        'get_tags'
    )

    def get_ingredients(self, obj):
        return "\n".join([str(p) for p in obj.ingredients.all()])

    def get_tags(self, obj):
        return ", ".join([str(p) for p in obj.tags.all()])

    get_ingredients.short_description = "Ингредиенты"
    get_tags.short_description = "Tags"
