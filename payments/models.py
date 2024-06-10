import uuid

from django.db import models

from relations.models import UserCottageRent


class Payment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, db_index=True)
    rent = models.ForeignKey(UserCottageRent, on_delete=models.CASCADE, related_name='payments', db_index=True)
    ukassa_id = models.CharField(max_length=100, db_index=True)
    redirect_url = models.URLField(db_index=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, db_index=True)
    status = models.CharField(max_length=50, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    ukassa_response = models.JSONField(db_index=True)

    class Meta:
        verbose_name = 'Платёж'
        verbose_name_plural = 'Платежи'

    def __str__(self):
        return f'Payment {self.id} for rent {self.rent}'
