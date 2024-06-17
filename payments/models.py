import datetime
import uuid
from decimal import Decimal

from django.conf import settings
from django.db import models, transaction
from yookassa import Configuration
from yookassa import Payment as UkassaPayment

from relations.models import UserCottageRent

Configuration.account_id = settings.SHOP_ID
Configuration.secret_key = settings.SHOP_SECRET


class PaymentManager(models.Manager):

    def create_payment(self, rent: UserCottageRent, return_url: str = 'localhost:8000/cottages'):
        """ Create Payment and add it to DB """
        ukassa_payment = self._create_ukassa_payment(rent, return_url)
        new_payment = self.create(
            rent=rent,
            amount=ukassa_payment.amount.value,
            ukassa_id=ukassa_payment.id,
            redirect_url=ukassa_payment.confirmation["confirmation_url"],
            status=ukassa_payment.status,
            created_at=datetime.datetime.now(),
            ukassa_response=ukassa_payment.json()
        )
        return new_payment

    @staticmethod
    def _create_ukassa_payment(rent: UserCottageRent, return_url: str) -> UkassaPayment:
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


class Payment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, db_index=True)
    rent = models.ForeignKey(UserCottageRent, on_delete=models.CASCADE, related_name='payments', db_index=True)
    ukassa_id = models.CharField(max_length=100, db_index=True)
    redirect_url = models.URLField(db_index=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, db_index=True)
    status = models.CharField(max_length=50, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    ukassa_response = models.JSONField(db_index=True)

    objects = PaymentManager()

    class Meta:
        verbose_name = 'Платёж'
        verbose_name_plural = 'Платежи'

    def __str__(self):
        return f'Payment {self.id} for rent {self.rent}'

    def change_payment_status(self, status: str):
        with transaction.atomic():
            self.status = status
            self.save()
            self.rent.status = 2 if status == "succeeded" else 3
            self.rent.save()
