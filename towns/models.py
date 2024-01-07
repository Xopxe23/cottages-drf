import os
import uuid

from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver


class Town(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, unique=True, verbose_name="Название")
    description = models.TextField(verbose_name="Описание")

    class Meta:
        verbose_name = 'Населенный пункт'
        verbose_name_plural = 'Населенные пункты'

    def __str__(self):
        return self.name


def town_image_path(instance, filename):
    town_id = instance.town.id
    return os.path.join("town_images", str(town_id), filename)


class TownImage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    town = models.ForeignKey(Town, on_delete=models.CASCADE, related_name="images", verbose_name="Населенный пункт")
    image = models.ImageField(upload_to=town_image_path, verbose_name="Фотография")

    class Meta:
        verbose_name = 'Фотография населенного пункта'
        verbose_name_plural = 'Фотография населенного пункта'

    def __str__(self):
        return f'Photo for {self.town}'


@receiver(pre_delete, sender=TownImage)
def delete_cottage_image(sender, instance, **kwargs):
    instance.image.delete(False)


class TownAttraction(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    town = models.ForeignKey(Town, on_delete=models.CASCADE, related_name="attractions",
                             verbose_name="Населенный пункт")
    name = models.CharField(max_length=255, verbose_name="Название")
    description = models.TextField(verbose_name="Описание")

    class Meta:
        verbose_name = 'Достопримечательность'
        verbose_name_plural = 'Достопримечательности'

    def __str__(self):
        return self.name


def attraction_image_path(instance, filename):
    attraction_id = instance.attraction.id
    return os.path.join("attraction_images", str(attraction_id), filename)


class AttractionImage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    attraction = models.ForeignKey(TownAttraction, on_delete=models.CASCADE, related_name="images",
                                   verbose_name="Достопримечательнось")
    image = models.ImageField(upload_to=attraction_image_path, verbose_name="Фотография")

    class Meta:
        verbose_name = 'Фотография достопримечательности'
        verbose_name_plural = 'Фотографии достопримечательности'

    def __str__(self):
        return f'Photo for {self.attraction}'
