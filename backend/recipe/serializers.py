import os.path

from django.shortcuts import get_object_or_404
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from users.serializers import UserSerializer

from .models import (Favorite, IngredientAmount, Ingredients, Recipe,
                     ShoppingCart, Tag)


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class IngredientsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredients
        fields = ('id', 'name', 'measurement_unit')


class IngredientAmountSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = IngredientAmount
        fields = ('id', 'name', 'measurement_unit', 'amount')
        validators = [
            UniqueTogetherValidator(
                queryset=IngredientAmount.objects.all(),
                fields=['ingredient', 'recipe']
            )
        ]


class RecipeSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    ingredients = IngredientAmountSerializer(
        source="ingredientamount_set",
        read_only=True,
        many=True,
    )
    author = UserSerializer(read_only=True)
    image = Base64ImageField()
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'name',
            'image',
            'text',
            'cooking_time',
            'is_favorited',
            'is_in_shopping_cart'
        )

    def get_is_in_shopping_cart(self, obj):
        user = self.context["request"].user
        if user.is_authenticated:
            return (
                ShoppingCart.objects.filter(
                    author=user, recipe_id=obj.id
                ).exists()
            )
        return False

    def get_is_favorited(self, obj):
        user = self.context["request"].user
        if user.is_authenticated:
            return Favorite.objects.filter(
                author=user, recipe_id=obj.id
            ).exists()
        return False

    def validate(self, data):
        image = self.initial_data.get('image')
        ingredients = self.initial_data.get('ingredients')
        max_upload_size = 5242880
        if os.path.getsize(image) > max_upload_size:
            raise serializers.ValidationError(
                'Размер загружаемого файла не более 5мб'
            )
        if not ingredients:
            raise serializers.ValidationError({
                'ingredients': 'Рецепт не может быть без ингредиентов'})
        ingredient_list = []
        for ingredient_it in ingredients:
            ingredient = get_object_or_404(
                Ingredients,
                id=ingredient_it['id']
            )
            if ingredient in ingredient_list:
                raise serializers.ValidationError(
                    'В одном рецепте ингредиенты не могут повторяться'
                )
            ingredient_list.append(ingredient)
            if int(ingredient_it['amount']) < 0:
                raise serializers.ValidationError({
                    'ingredients': (
                        'Количество ингредиента не может быть меньше 0'
                    )
                })
            if str(ingredient_it).isalpha() or str(ingredient_it).isalnum():
                raise serializers.ValidationError(
                    'Колличество нужно указывать только в цифрах'
                )
        data['ingredients'] = ingredients
        return data

    def create_ingredients(self, ingredients, recipe):
        IngredientAmount.objects.bulk_create(
            [IngredientAmount(
                recipe=recipe,
                ingredient_id=ingredient.get('id'),
                amount=ingredient.get('amount')
            ) for ingredient in ingredients]
        )

    def create(self, validated_data):
        image = validated_data.pop('image')
        ingredients_data = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(image=image, **validated_data)
        tags_data = self.initial_data.get('tags')
        recipe.tags.set(tags_data)
        self.create_ingredients(ingredients_data, recipe)
        return recipe

    def update(self, instance, validated_data):
        instance.image = validated_data.get('image', instance.image)
        instance.name = validated_data.get('name', instance.name)
        instance.text = validated_data.get('text', instance.text)
        instance.cooking_time = validated_data.get(
            'cooking_time', instance.cooking_time
        )
        instance.tags.clear()
        tags_data = self.initial_data.get('tags')
        instance.tags.set(tags_data)
        IngredientAmount.objects.filter(recipe=instance).all().delete()
        self.create_ingredients(validated_data.get('ingredients'), instance)
        instance.save()
        return instance
