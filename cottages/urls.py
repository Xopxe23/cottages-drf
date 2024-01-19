from django.urls import path
from django.views.decorators.cache import cache_page

from cottages.views import CreateCottageView, ListCottageView, RetrieveUpdateDestroyCottageView, UpdateCottageImageOrder
from relations.views import ListUserCottageReviewView, UpdateDestroyReviewView

urlpatterns = [
    path('create/', CreateCottageView.as_view(), name='cottages-create'),
    path('', cache_page(30)(ListCottageView.as_view()), name='cottages-list'),
    path('<uuid:pk>/', cache_page(30)(RetrieveUpdateDestroyCottageView.as_view()), name='cottages-detail'),
    path('<uuid:cottage_id>/reviews/', ListUserCottageReviewView.as_view(), name='reviews-list'),
    path('<uuid:cottage_id>/reviews/<uuid:pk>/', UpdateDestroyReviewView.as_view(), name='reviews-detail'),
    path('images/change_order/', UpdateCottageImageOrder.as_view(), name='images-update')
]
