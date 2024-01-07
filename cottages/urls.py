from django.urls import path

from cottages.views import CreateCottageView, ListCottageView, RetrieveUpdateCottageView

urlpatterns = [
    path('create/', CreateCottageView.as_view(), name='cottage-create'),
    path('', ListCottageView.as_view(), name='cottage-list'),
    path('<uuid:pk>/', RetrieveUpdateCottageView.as_view(), name='cottage-detail')
]
