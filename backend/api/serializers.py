from rest_framework import serializers
from .models import Category, FavoriteThing, Metadata
import logging

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name')

class FavoriteThingSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(source='category',  queryset=Category.objects.all(), write_only=True)

    class Meta:
        model = FavoriteThing
        fields = ('id', 'title', 'description', 'ranking', 'created_date', 'modified_date', 'audit_log', 'category', 'category_id')

class MetadataSerializer(serializers.ModelSerializer):
    favorite_thing = serializers.PrimaryKeyRelatedField(queryset=FavoriteThing.objects.all(), write_only=True)
    class Meta:
        model = Metadata
        fields = ('id', 'key', 'type', 'value', 'favorite_thing')
