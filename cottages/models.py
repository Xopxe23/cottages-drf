import uuid

from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from users.models import EmailUser


class OptionsValidator:
    def __init__(self, pool=False, parking=False, air_conditioning=False, wifi=False):
        self.pool = pool
        self.parking = parking
        self.air_conditioning = air_conditioning
        self.wifi = wifi

    def __call__(self, value):
        required_keys = {'pool', 'parking', 'air_conditioning', 'wifi'}
        if (not isinstance(value, dict) or set(value.keys()) != required_keys or not all(
                isinstance(value[key], bool) for key in value)):
            raise ValidationError('Invalid options format. Should be a dictionary with keys: '
                                  'pool, parking, air_conditioning, wifi.')


class Cottage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(EmailUser, on_delete=models.CASCADE)
    address = models.CharField(max_length=255)
    latitude = models.FloatField(validators=[MinValueValidator(-90), MaxValueValidator(90)])
    longitude = models.FloatField(validators=[MinValueValidator(-180), MaxValueValidator(180)])
    options = models.JSONField(default=dict, validators=[OptionsValidator()])

    def __str__(self):
        return f'Cottage {self.pk} - {self.address}'
