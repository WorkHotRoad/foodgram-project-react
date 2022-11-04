from django.contrib import admin
from .models import (
    Tag, Ingredients, Recipe,
    ShoppingCart, Favorite,
)

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "color",
        "slug",
    )
    list_editable = ("name", "color", "slug",)
    search_fields = ('name', 'slug', )


@admin.register(Ingredients)
class IngredientsAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "measurement_unit",
    )
    list_editable = ("name", "measurement_unit",)
    search_fields = ('name', )


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        "author",
        "name",
        'count_favorites'
    )
    list_filter = ('name', 'author', 'tags',)
    list_editable = ("name",)
    search_fields = ("name",)

    def count_favorites(self, obj):
        return obj.favorites.count()
    
    count_favorites.short_description = "Число добавлений в избранное"


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('author', 'recipe',)
    list_filter = ('author', 'recipe',)


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('author', 'recipe',)
    list_filter = ('author', 'recipe',)
