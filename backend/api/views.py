from re import T
from .models import Tag
from rest_framework import viewsets 
from rest_framework.response import Response
from .serializers import TagSerializer
from django.shortcuts import get_object_or_404


class TagViewSet(viewsets.ViewSet):
    def list(self, request):
        queryset = Tag.objects.all()
        serializer = TagSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Tag.objects.all()
        tag = get_object_or_404(queryset, pk=pk)
        serializer = TagSerializer(tag)
        return Response(serializer.data)
