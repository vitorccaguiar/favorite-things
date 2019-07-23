from rest_framework import routers
from .api.viewsets import CategoryViewSet, FavoriteThingViewSet, MetadataViewSet

router = routers.SimpleRouter()
router.register(r'category', CategoryViewSet)
router.register(r'favoritething', FavoriteThingViewSet)
router.register(r'metadata', MetadataViewSet)
