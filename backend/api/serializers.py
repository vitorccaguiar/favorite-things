from rest_framework import serializers
from .models import Category, FavoriteThing, Metadata, AuditLog
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
        fields = ('id', 'title', 'description', 'ranking', 'created_date', 'modified_date', 'category', 'category_id')

    def create(self, validated_data):
        obj = FavoriteThing.objects.create(**validated_data)
        AuditLog.objects.create(action_performed='POST', favorite_thing=obj)
        return obj

    def update(self, instance, validated_data):
        FavoriteThing.objects.update(instance)
        AuditLog.objects.create(action_performed='PUT', favorite_thing=instance)
        return instance

class MetadataSerializer(serializers.ModelSerializer):
    favorite_thing = serializers.PrimaryKeyRelatedField(queryset=FavoriteThing.objects.all(), write_only=True)
    class Meta:
        model = Metadata
        fields = ('id', 'key', 'type', 'value', 'favorite_thing')

class AuditLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuditLog
        fields = ('id', 'action_performed', 'created_date', 'favorite_thing')
