from django.urls import path
from django.views.decorators.cache import cache_page

from cottages.views import CreateCottageView, ListCottageView, RetrieveUpdateDestroyCottageView, UpdateCottageImageOrder
from relations.views import CreateUserCottageRent, ListUserCottageReviewView, UpdateDestroyReviewView

urlpatterns = [
    path('create/', CreateCottageView.as_view(), name='cottages-create'),
    path('', (ListCottageView.as_view()), name='cottages-list'),
    path('<uuid:pk>/', (RetrieveUpdateDestroyCottageView.as_view()), name='cottages-detail'),
    path('<uuid:cottage_id>/reviews/', ListUserCottageReviewView.as_view(), name='reviews-list'),
    path('<uuid:cottage_id>/reviews/<uuid:pk>/', UpdateDestroyReviewView.as_view(), name='reviews-detail'),
    path('<uuid:cottage_id>/create_rent/', CreateUserCottageRent.as_view(), name='rents-create'),
    path('images/change_order/', UpdateCottageImageOrder.as_view(), name='images-update')
]
