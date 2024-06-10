from django.urls import path

from payments.views import change_payment_status_view, get_payment_status_view

urlpatterns = [
    path('<uuid:payment_id>/', get_payment_status_view, name='get-status'),
    path('update_status/', change_payment_status_view, name='update-status')
]
