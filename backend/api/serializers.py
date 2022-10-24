# import webcolors
from rest_framework import serializers
from .models import Tag


# class Hex2NameColor(serializers.Field):
    
#     def to_representation(self, value):
#         value = webcolors.name_to_hex(value)
#         return value
    
#     def to_internal_value(self, data):
#         try:
#             data = webcolors.name_to_hex(data)
#         except ValueError:
#             raise serializers.ValidationError('Нет такого цвета')
#         return data


class TagSerializer(serializers.ModelSerializer):
    # color = Hex2NameColor()
    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')