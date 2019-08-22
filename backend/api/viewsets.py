from rest_framework import viewsets
from .models import Category, FavoriteThing, Metadata, AuditLog
from .serializers import CategorySerializer, FavoriteThingSerializer, MetadataSerializer, AuditLogSerializer

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class FavoriteThingViewSet(viewsets.ModelViewSet):
    queryset = FavoriteThing.objects.all()
    serializer_class = FavoriteThingSerializer

class MetadataViewSet(viewsets.ModelViewSet):
    queryset = Metadata.objects.all()
    serializer_class = MetadataSerializer

    def get_queryset(self):
        if 'favorite_thing' in self.request.QUERY_PARAMS:
            favorite_thing = self.request.query_params.get('favorite_thing')
            return Metadata.objects.all().filter(favorite_thing__id=favorite_thing)
        else:
            return Metadata.objects.all()

class AuditLogViewSet(viewsets.ModelViewSet):
    queryset = AuditLog.objects.all()
    serializer_class = AuditLogSerializer