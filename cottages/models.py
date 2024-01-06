import os
import uuid

from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver

from users.models import EmailUser


def validate_options(value):
    required_keys = {'pool', 'parking', 'air_conditioning', 'wifi'}
    if (not isinstance(value, dict) or set(value.keys()) != required_keys or not all(
            isinstance(value[key], bool) for key in value)):
        raise ValidationError('Invalid options format. Should be a dictionary with keys:'
                              ' pool, parking, air_conditioning, wifi.')


def cottage_image_path(instance, filename):
    # instance - экземпляр модели CottageImage, filename - имя файла
    cottage_id = instance.cottage.id
    return os.path.join("cottage_images", str(cottage_id), filename)


class Cottage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(EmailUser, on_delete=models.CASCADE)
    price = models.PositiveIntegerField(validators=[MaxValueValidator(50000)])
    address = models.CharField(max_length=255)
    latitude = models.FloatField(validators=[MinValueValidator(-90), MaxValueValidator(90)])
    longitude = models.FloatField(validators=[MinValueValidator(-180), MaxValueValidator(180)])
    options = models.JSONField(default=dict, validators=[validate_options])

    def __str__(self):
        return f'Cottage {self.pk} - {self.address}'


class CottageImage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    cottage = models.ForeignKey(Cottage, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to=cottage_image_path)


@receiver(pre_delete, sender=CottageImage)
def delete_cottage_image(sender, instance, **kwargs):
    # Удалить файл изображения
    instance.image.delete(False)


class CottageComment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    cottage = models.ForeignKey(Cottage, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(EmailUser, on_delete=models.CASCADE, related_name="comments")
    comment = models.TextField()
    rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
