from django.urls import path
from django.views.decorators.cache import cache_page

from cottages.views import CreateCottageView, ListCottageView, RetrieveUpdateDestroyCottageView

urlpatterns = [
    path('create/', CreateCottageView.as_view(), name='cottage-create'),
    path('', cache_page(30)(ListCottageView.as_view()), name='cottage-list'),
    path('<uuid:pk>/', cache_page(30)(RetrieveUpdateDestroyCottageView.as_view()), name='cottage-detail')
]
