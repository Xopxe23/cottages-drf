from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedSimpleRouter

from .views import TownAttractionViewSet, TownViewSet, update_attraction_image_order, update_town_image_order

router = DefaultRouter()
router.register(r'', TownViewSet, basename='towns')

attractions_router = NestedSimpleRouter(router, r'', lookup='town')
attractions_router.register(r'attractions', TownAttractionViewSet, basename='attractions')

urlpatterns = router.urls + attractions_router.urls

urlpatterns += [
    path('images/change_order/', update_town_image_order, name='images-update'),
    path('attractions/images/change_order/', update_attraction_image_order, name='images-update')
]
