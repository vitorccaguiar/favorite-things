from rest_framework import serializers
from .models import Category, FavoriteThing, Metadata, AuditLog
import logging

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name')

    def create(self, validated_data):
        Category.objects.create(**validated_data)
        Category.objects.create(related_model_name='Category', action_performed='POST', favorite_thing=validated_data['id'])

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

class AuditLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuditLog
        fields = ('id', 'related_model_name', 'action_performed', 'created_date', 'favorite_thing')
