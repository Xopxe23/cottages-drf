from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedSimpleRouter

from .views import TownAttractionViewSet, TownViewSet, UpdateAttractionImageOrder, UpdateTownImageOrder

router = DefaultRouter()
router.register(r'', TownViewSet, basename='towns')

attractions_router = NestedSimpleRouter(router, r'', lookup='town')
attractions_router.register(r'attractions', TownAttractionViewSet, basename='attractions')

urlpatterns = router.urls + attractions_router.urls

urlpatterns += [
    path('images/change_order/', UpdateTownImageOrder.as_view(), name='images-update'),
    path('attractions/images/change_order/', UpdateAttractionImageOrder.as_view(), name='images-update')
]
