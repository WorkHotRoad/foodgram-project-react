from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from prettytable import PrettyTable
from rest_framework import filters, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from users.serializers import FavoritRecipeSerializer
from users.pagination import LimitPageNumberPagination


from .models import (Favorite, IngredientAmount, Ingredients, Recipe,
                     ShoppingCart, Tag)
from users.models import Follow
from .permissions import IsAdminOrReadOnly, OwnerOrReadOnly
from .serializers import IngredientsSerializer, RecipeSerializer, TagSerializer





class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = None


class IngredientsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredients.objects.all()
    serializer_class = IngredientsSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter, )
    search_fields = ('^name',)
    pagination_class = None

    def get_queryset(self):
        queryset = self.queryset
        name = self.request.GET.get('name')
        if name:
            return Ingredients.objects.filter(name__istartswith=name)
        return queryset


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = [OwnerOrReadOnly]
    pagination_class = LimitPageNumberPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_queryset(self):
        queryset = self.queryset
        tags = self.request.query_params.getlist('tags')
        
        queryset = queryset.filter(tags__slug__in=tags).distinct()

        author = self.request.query_params.get('author')
        if author:
            queryset = queryset.filter(author=author)
        
        user = self.request.user
        if user.is_authenticated:
            is_favorited = self.request.GET.get('is_favorited')
            is_in_shopping_cart = self.request.GET.get('is_in_shopping_cart')
            if is_favorited:
                queryset = Recipe.objects.filter(favorites__author=self.request.user)
                return queryset
            if is_in_shopping_cart:
                queryset = Recipe.objects.filter(Shopping_list__author=self.request.user)
                return queryset
        return queryset

    @action(
        detail=True, methods=['post', 'delete'],
        permission_classes=(permissions.IsAuthenticated,)
    )
    def shopping_cart(self, request, pk=None):
        customer = self.request.user
        tag = "покупок"
        if request.method == 'POST':
            return self.func_add_object(ShoppingCart, customer, tag, pk)
        if request.method == 'DELETE':
            return self.func_delete_object(ShoppingCart, customer, tag, pk)
        return None

    @action(
        detail=True, methods=['post', 'delete'],
        permission_classes=(permissions.IsAuthenticated,)
    )
    def favorite(self, request, pk=None,):
        customer = self.request.user
        tag = "избранного"
        if request.method == 'POST':
            return self.func_add_object(Favorite, customer, tag, pk)
        if request.method == 'DELETE':
            return self.func_delete_object(Favorite, customer, tag, pk)
        return None

    @action(detail=False, methods=['get'],
            permission_classes=[permissions.IsAuthenticated])
    def download_shopping_cart(self, request):
        user = request.user
        recipe_query = ShoppingCart.objects.filter(
            author=user
        ).values('recipe__name')
        if len(recipe_query):
            recipe_list = ", ".join(
                [values for i in recipe_query for keys, values in i.items()]
            )
            ingredients = IngredientAmount.objects.filter(
                recipe__Shopping_list__author=user).values(
                'ingredient__name',
                'ingredient__measurement_unit').annotate(total=Sum('amount'))

            shopping_body = [
                values for i in ingredients for keys, values in i.items()
            ]
            shopping_head = ['Продукт', 'Ед.измерения', 'Кол-во']
            columns = len(shopping_head)
            table = PrettyTable(shopping_head)
            while shopping_body:
                columns = len(shopping_head)
                table.add_row(shopping_body[:columns])
                shopping_body = shopping_body[columns:]
            file = (
                f"Вот что вам нужно купить для выбранных рецептов\n"
                f"Рецепты: {recipe_list}\n\n"
            )
            file += str(table)
            filename = "shopping_list.txt"
            response = HttpResponse(file, content_type='text/plain')
            response[
                'Content-Disposition'
            ] = f'attachment; filename={filename}'

            return response
        return Response({
            'errors': 'Нет рецептов в списке'},
            status=status.HTTP_400_BAD_REQUEST)

    def func_add_object(self, model, user, tag, pk):
        if model.objects.filter(author=user, recipe__id=pk).exists():
            return Response({
                'errors': f'Рецепт уже в списке {tag}'
            }, status=status.HTTP_400_BAD_REQUEST)
        recipe = get_object_or_404(Recipe, id=pk)
        model.objects.create(author=user, recipe=recipe)
        serializer = FavoritRecipeSerializer(recipe)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def func_delete_object(self, model, user, tag, pk):
        obj = model.objects.filter(author=user, recipe__id=pk)
        if obj.exists():
            obj.delete()
            return Response({
                f'Рецепт удален из списка {tag}'
            }, status=status.HTTP_204_NO_CONTENT)
        return Response({
            'errors': 'Рецепт уже удален'
        }, status=status.HTTP_400_BAD_REQUEST)
