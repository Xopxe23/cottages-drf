from uuid import UUID

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response
from yookassa.domain.notification import WebhookNotification

from payments.models import Payment
from payments.serializers import PaymentSerializer


@api_view(["GET"])
def get_payment_status_view(request: Request, payment_id: UUID) -> Response:
    payment = Payment.objects.filter(id=payment_id).first()
    serializer = PaymentSerializer(payment)
    if payment:
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)
    return Response({"error": "payment not exists"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def change_payment_status_view(request: Request) -> Response:
    data = request.data
    try:
        notification_object = WebhookNotification(data)
    except Exception:
        return Response({"status": "error webhook"}, status=status.HTTP_400_BAD_REQUEST)
    ukassa_info = notification_object.object
    ukassa_id = ukassa_info.id
    ukassa_status = ukassa_info.status
    payment = Payment.objects.select_related("rent").filter(ukassa_id=ukassa_id)
    payment.change_payment_status(ukassa_status)
    return Response(status.HTTP_204_NO_CONTENT)
