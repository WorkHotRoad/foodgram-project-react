from .models import Tag, Ingredients
from rest_framework import viewsets 
from rest_framework.response import Response
from .serializers import TagSerializer, IngredientsSerializer
from django.shortcuts import get_object_or_404
from rest_framework import filters



class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    filter_backends = (filters.SearchFilter, )
    search_fields = ('name',)


class IngredientsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredients.objects.all()
    serializer_class = IngredientsSerializer
    filter_backends = (filters.SearchFilter, )
    search_fields = ('name',)


# class TagViewSet(viewsets.ViewSet):
#     def list(self, request):
#         queryset = Tag.objects.all()
#         serializer = TagSerializer(queryset, many=True)
#         return Response(serializer.data)

#     def retrieve(self, request, pk=None):
#         queryset = Tag.objects.all()
#         tag = get_object_or_404(queryset, pk=pk)
#         serializer = TagSerializer(tag)
#         return Response(serializer.data)