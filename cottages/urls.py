from django.urls import path

from cottages.views import CreateCottageView, ListCottageView, RetrieveUpdateDestroyCottageView

urlpatterns = [
    path('create/', CreateCottageView.as_view(), name='cottage-create'),
    path('', ListCottageView.as_view(), name='cottage-list'),
    path('<uuid:pk>/', RetrieveUpdateDestroyCottageView.as_view(), name='cottage-detail')
]
