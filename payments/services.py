import datetime
from decimal import Decimal

from django.conf import settings
from django.db import transaction
from yookassa import Configuration
from yookassa import Payment as UkassaPayment

from payments.models import Payment
from relations.models import UserCottageRent

Configuration.account_id = settings.SHOP_ID
Configuration.secret_key = settings.SHOP_SECRET


def create_ukassa_payment(rent: UserCottageRent, return_url: str) -> UkassaPayment:
    """ Create IOKassa payment and return it """
    payment = UkassaPayment.create({
        "amount": {
            "value": Decimal(str(rent.cottage.price)),
            "currency": "RUB"
        },
        "confirmation": {
            "type": "redirect",
            "return_url": return_url
        },
        "capture": True,
        "description": rent.__str__()
    }, rent.id)
    return payment


def create_payment(rent: UserCottageRent, return_url: str):
    """ Create Payment and add it to DB """
    ukassa_payment = create_ukassa_payment(rent, return_url)
    new_payment = Payment.objects.create(
        rent=rent,
        amount=ukassa_payment.amount.value,
        ukassa_id=ukassa_payment.id,
        redirect_url=ukassa_payment.confirmation["confirmation_url"],
        status=ukassa_payment.status,
        created_at=datetime.datetime.now(),
        ukassa_response=ukassa_payment.json()
    )
    return new_payment


def change_payment_status(payment: Payment, status: str) -> None:
    """Change payment and rent status"""
    with transaction.atomic():
        payment.status = status
        payment.save()
        payment.rent.status = 2 if status == "succeeded" else 3
        payment.rent.save()
