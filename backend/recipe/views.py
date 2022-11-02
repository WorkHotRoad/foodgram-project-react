from .models import Tag, Ingredients, Recipe, Favorite
from .permissions import IsAdminOrReadOnly, IsAdminOwnerOrReadOnly
from rest_framework.response import Response
from .serializers import TagSerializer, IngredientsSerializer, RecipeSerializer
from users.serializers import FavoritRecipeSerializer
from django.shortcuts import get_object_or_404
from rest_framework import filters, permissions, status, viewsets
from rest_framework.decorators import action


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter, )
    search_fields = ('name',)


class IngredientsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredients.objects.all()
    serializer_class = IngredientsSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (filters.SearchFilter, )
    search_fields = ('name',)


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all().order_by('-id')
    serializer_class = RecipeSerializer
    permission_classes = [IsAdminOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


    @action(
        detail=True, methods=['post', 'delete'],
        permission_classes=(permissions.IsAuthenticated,)
    )
    def favorite(self, request, pk=None,):
        customer = self.request.user
        if request.method == 'POST':
            if Favorite.objects.filter(author=customer, recipe__id=pk).exists():
                return Response({
                    'errors': 'Рецепт уже в избранном'
                }, status=status.HTTP_400_BAD_REQUEST)
            recipe = get_object_or_404(Recipe, id=pk)
            Favorite.objects.create(author=customer, recipe=recipe)
            serializer = FavoritRecipeSerializer(recipe)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            obj = Favorite.objects.filter(author=customer, recipe__id=pk)
            if obj.exists():
                obj.delete()
                return Response({
                    'Рецепт удален из избранного'
                },status=status.HTTP_204_NO_CONTENT)
            return Response({
                'errors': 'Рецепт уже удален'
            }, status=status.HTTP_400_BAD_REQUEST)
