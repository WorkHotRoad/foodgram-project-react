
from drf_extra_fields.fields import Base64ImageField

from djoser.serializers import UserCreateSerializer
from django.shortcuts import get_object_or_404
from recipe.models import Recipe
from rest_framework import serializers

from .models import Follow, User


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
        request = self.context['request']
        if request.user.is_anonymous:
            return False
        return Follow.objects.filter(user=request.user, following=obj).exists()


class FavoritRecipeSerializer(serializers.ModelSerializer):
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class ShowFollowsSerializer(UserSerializer):
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name',
                  'last_name', 'is_subscribed', 'recipes', 'recipes_count')

    def get_recipes(self, obj):
        queryset = Recipe.objects.filter(author=obj)
        request = self.context['request']
        limit = request.GET.get('recipes_limit')
        if limit:
            queryset = queryset[:int(limit)]
        return FavoritRecipeSerializer(queryset, many=True).data

    def get_recipes_count(self, obj):
        queryset = Recipe.objects.filter(author=obj)
        return queryset.count()


class FollowSerializer(serializers.ModelSerializer):
    user = serializers.IntegerField(source='user.id')
    following = serializers.IntegerField(source='following.id')

    class Meta:
        model = Follow
        fields = ['user', 'following']

    def validate(self, data):
        user = data['user']['id']
        following = data['following']['id']
        follow_exist = Follow.objects.filter(
            user=user, following__id=following
        ).exists()
        if user == following:
            raise serializers.ValidationError(
                {"errors": 'Вы не можете подписаться на самого себя'}
            )
        elif follow_exist:
            raise serializers.ValidationError({"errors": 'Вы уже подписаны'})
        return data

    def create(self, validated_data):
        following = validated_data.get('following')
        following = get_object_or_404(User, pk=following.get('id'))
        user = validated_data.get('user')
        return Follow.objects.create(user=user, following=following)
