from django.urls import path, include
from rest_framework.routers import DefaultRouter

from cottages.views import (
    # ListCottageView,
    # create_cottage_view,
    # update_cottage_view,
    # retrieve_cottage_view,
    update_cottage_image_order, CottageViewSet,
)
from relations.views import (
    # ListUserCottageReviewView,
    # UpdateDestroyReviewView,
    add_or_remove_favorites,
    create_cottage_rent_view,
    get_current_user_cottages_view,
    get_current_user_favorites,
    get_current_user_rents_view, UserCottageReviewViewSet,
)

cottage_router = DefaultRouter()
cottage_router.register(r'', CottageViewSet, basename='cottages')

review_router = DefaultRouter()
review_router.register(r'reviews', UserCottageReviewViewSet, basename='reviews')

urlpatterns = [
    path('', include(cottage_router.urls)),
    path('<uuid:cottage_id>/', include(review_router.urls)),
    # path('', (ListCottageView.as_view()), name='cottages-list'),
    # path('create/', create_cottage_view, name='cottages-create'),
    # path('update/', update_cottage_view, name='cottages-update'),
    # path('<uuid:pk>/', retrieve_cottage_view, name='cottages-detail'),
    # path('<uuid:pk>/', delete_cottage_view, name='cottages-delete'),
    # path('<uuid:cottage_id>/reviews/', ListUserCottageReviewView.as_view(), name='reviews-list'),
    # path('<uuid:cottage_id>/reviews/<uuid:pk>/', UpdateDestroyReviewView.as_view(), name='reviews-detail'),
    path('<uuid:cottage_id>/create_rent/', create_cottage_rent_view, name='rents-create'),
    path('<uuid:cottage_id>/favorites/', add_or_remove_favorites, name='favorites'),
    path('my_favorites/', get_current_user_favorites, name='my-favorites'),
    path('my_rents/', get_current_user_rents_view, name='my-rents'),
    path('my_cottages/', get_current_user_cottages_view, name='my-cottages'),
    path('images/change_order/', update_cottage_image_order, name='images-update')
]
