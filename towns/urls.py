from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedSimpleRouter

from .views import TownAttractionViewSet, TownViewSet

router = DefaultRouter()
router.register(r'', TownViewSet, basename='towns')

attractions_router = NestedSimpleRouter(router, r'', lookup='town')
attractions_router.register(r'attractions', TownAttractionViewSet, basename='attractions')

urlpatterns = router.urls + attractions_router.urls
