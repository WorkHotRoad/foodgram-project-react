
from drf_extra_fields.fields import Base64ImageField

from djoser.serializers import UserCreateSerializer
from recipe.models import Recipe
from rest_framework import serializers

from .models import Follow


class CustomUserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        fields = (
            'email', 'id', 'username',
            'first_name', 'last_name',
            'password',
        )
        read_only_fields = ('id', )


class UserSerializer(UserCreateSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta(UserCreateSerializer.Meta):
        fields = (
            'email', 'id', 'username',
            'first_name', 'last_name',
            'is_subscribed',
        )

    def get_is_subscribed(self, obj):
        user = self.context.get('request').user
        if user.is_authenticated:
            return Follow.objects.filter(
                user=user, following=obj.id
            ).exists()
        return False


class FavoritRecipeSerializer(serializers.ModelSerializer):
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class FollowSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='following.id')
    email = serializers.ReadOnlyField(source='following.email')
    username = serializers.ReadOnlyField(source='following.username')
    first_name = serializers.ReadOnlyField(source='following.first_name')
    last_name = serializers.ReadOnlyField(source='following.last_name')
    is_subscribed = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = Follow
        fields = (
            'email', 'id', 'username',
            'first_name', 'last_name',
            'is_subscribed', 'recipes',
            'recipes_count'
        )

    def get_is_subscribed(self, obj):
        return Follow.objects.filter(
            user=obj.user, following=obj.following
        ).exists()

    def get_recipes(self, obj):
        request = self.context.get('request')
        limit = request.GET.get('recipes_limit')
        queryset = Recipe.objects.filter(author=obj.following)
        if limit:
            queryset = queryset[:int(limit)]
        return FavoritRecipeSerializer(queryset, many=True).data
        # recipe = Recipe.objects.filter(author=obj.following)
        # return FavoritRecipeSerializer(recipe, many=True).data

    def get_recipes_count(self, obj):
        return Recipe.objects.filter(author=obj.following).count()
