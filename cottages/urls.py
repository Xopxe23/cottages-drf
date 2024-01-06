from django.urls import path

from cottages.views import CreateCottageView, ListCottagesView, RetrieveUpdateCottageView

urlpatterns = [
    path('create/', CreateCottageView.as_view(), name='cottage-create'),
    path('', ListCottagesView.as_view(), name='cottage-list'),
    path('<uuid:pk>/', RetrieveUpdateCottageView.as_view(), name='cottage-detail')
]
