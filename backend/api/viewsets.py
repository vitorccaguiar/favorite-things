from rest_framework import viewsets
from .models import Category, FavoriteThing, Metadata
from .serializers import CategorySerializer, FavoriteThingSerializer, MetadataSerializer

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class FavoriteThingViewSet(viewsets.ModelViewSet):
    queryset = FavoriteThing.objects.all()
    serializer_class = FavoriteThingSerializer

class MetadataViewSet(viewsets.ModelViewSet):
    queryset = Metadata.objects.all()
    serializer_class = MetadataSerializer