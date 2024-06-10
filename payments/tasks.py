from uuid import UUID

from celery import shared_task
from yookassa import Payment as UkassaPayment

from payments.models import Payment
from payments.services import change_payment_status


@shared_task
def check_and_update_payment_status(payment_id: UUID):
    """Check status and update it for schedule"""
    payment = Payment.objects.select_related('rent').filter(id=payment_id).first()
    ukassa_payment = UkassaPayment.find_one(payment.ukassa_id)
    if ukassa_payment.status != payment.status:
        change_payment_status(payment, ukassa_payment.status)


@shared_task
def finally_update_payment_status(payment_id: UUID):
    """Check status and finally update it"""
    payment = Payment.objects.select_related('rent').filter(id=payment_id).first()
    if payment and payment.status != "succeeded":
        change_payment_status(payment, "canceled")


@shared_task
def schedule_check_and_update_payment_status(payment_id: UUID):
    """Check and update status every 10 minutes and finally check after hour"""
    for minute in range(0, 60, 10):
        check_and_update_payment_status.apply_async((payment_id,), countdown=minute * 60)
    finally_update_payment_status.apply_async((payment_id,), countdown=60 * 61)
