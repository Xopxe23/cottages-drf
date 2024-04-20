from django.urls import path
from django.views.decorators.cache import cache_page

from cottages.views import (
    CreateCottageView,
    ListCottageView,
    RetrieveUpdateDestroyCottageView,
    update_cottage_image_order,
)
from relations.views import (
    ListUserCottageReviewView,
    UpdateDestroyReviewView,
    add_or_remove_favorites,
    create_cottage_rent_view,
    get_current_user_cottages_view,
    get_current_user_favorites,
    get_current_user_rents_view,
)

urlpatterns = [
    path('create/', CreateCottageView.as_view(), name='cottages-create'),
    path('', (ListCottageView.as_view()), name='cottages-list'),
    path('<uuid:pk>/', (RetrieveUpdateDestroyCottageView.as_view()), name='cottages-detail'),
    path('<uuid:cottage_id>/reviews/', ListUserCottageReviewView.as_view(), name='reviews-list'),
    path('<uuid:cottage_id>/reviews/<uuid:pk>/', UpdateDestroyReviewView.as_view(), name='reviews-detail'),
    path('<uuid:cottage_id>/create_rent/', create_cottage_rent_view, name='rents-create'),
    path('<uuid:cottage_id>/favorites/', add_or_remove_favorites, name='favorites'),
    path('my_favorites/', get_current_user_favorites, name='my-favorites'),
    path('my_rents/', get_current_user_rents_view, name='my-rents'),
    path('my_cottages/', get_current_user_cottages_view, name='my-cottages'),
    path('images/change_order/', update_cottage_image_order, name='images-update')
]
