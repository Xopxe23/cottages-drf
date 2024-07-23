from django.urls import path

from .views import get_suggestion

urlpatterns = [
    path('', get_suggestion, name='get-suggest'),
]
