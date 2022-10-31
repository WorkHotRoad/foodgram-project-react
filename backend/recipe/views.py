from .models import Tag, Ingredients, Recipe
from .permissions import IsAdminOrReadOnly, IsAdminOwnerOrReadOnly
from rest_framework import viewsets 
from rest_framework.response import Response
from .serializers import TagSerializer, IngredientsSerializer, RecipeSerializer
from django.shortcuts import get_object_or_404
from rest_framework import filters, permissions


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
    
    