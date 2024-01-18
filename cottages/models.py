import os
import uuid

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from ordered_model.models import OrderedModel

from towns.models import Town
from users.models import User


class CottageCategory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, unique=True, verbose_name="Название")

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Cottage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    category = models.ForeignKey(CottageCategory, on_delete=models.CASCADE, verbose_name="Категория")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    name = models.CharField(max_length=255, verbose_name="Название")
    description = models.TextField(verbose_name="Описание")
    town = models.ForeignKey(Town, on_delete=models.CASCADE, verbose_name="Населенный пункт")
    address = models.CharField(max_length=255, null=True, blank=True, verbose_name="Адрес")
    price = models.PositiveIntegerField(validators=[MaxValueValidator(99999)], verbose_name="Цена")
    guests = models.PositiveIntegerField(validators=[MaxValueValidator(50)], verbose_name="Кол-во гостей")
    beds = models.PositiveIntegerField(validators=[MaxValueValidator(30)], verbose_name="Кол-во кроватей")
    rooms = models.PositiveIntegerField(validators=[MaxValueValidator(15)], verbose_name="Кол-во комнат")
    total_area = models.PositiveIntegerField(validators=[MaxValueValidator(500)], verbose_name="Общая площадь")
    latitude = models.FloatField(validators=[MinValueValidator(-90), MaxValueValidator(90)], verbose_name="Широта")
    longitude = models.FloatField(validators=[MinValueValidator(-180), MaxValueValidator(180)], verbose_name="Долгота")

    class Meta:
        verbose_name = 'Коттедж'
        verbose_name_plural = 'Коттеджи'

    def __str__(self):
        return f'{self.name} in {self.town.name}'


class CottageRules(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    cottage = models.OneToOneField(Cottage, on_delete=models.CASCADE, related_name="rules", verbose_name="Коттедж")
    check_in_time = models.TimeField(verbose_name="Время заезда")
    check_out_time = models.TimeField(verbose_name="Время выезда")
    with_children = models.BooleanField(default=True, verbose_name="С детьми")
    with_pets = models.BooleanField(default=False, verbose_name="С животными")
    smoking = models.BooleanField(default=False, verbose_name="Курение")
    parties = models.BooleanField(default=True, verbose_name="Вечеринки")
    need_documents = models.BooleanField(default=True, verbose_name="Необходимость документов")

    class Meta:
        verbose_name = 'Правила коттеджа'
        verbose_name_plural = 'Правила коттеджа'

    def __str__(self):
        return f"Rules for {self.cottage.name}"


class CottageAmenities(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    cottage = models.OneToOneField(Cottage, on_delete=models.CASCADE, related_name="amenities", verbose_name="Коттедж")
    parking_spaces = models.SmallIntegerField(validators=[MaxValueValidator(10)],
                                              verbose_name="Кол-во парковочных мест")
    wifi = models.BooleanField(default=False, verbose_name="Вай-фай")
    tv = models.BooleanField(default=False, verbose_name="Телевизор")
    air_conditioner = models.BooleanField(default=False, verbose_name="Кондиционер")
    hair_dryer = models.BooleanField(default=False, verbose_name="Фен")
    electric_kettle = models.BooleanField(default=False, verbose_name="Электрический чайник")

    class Meta:
        verbose_name = 'Удобства коттеджа'
        verbose_name_plural = 'Удобства коттеджа'

    def __str__(self):
        return f"Amenities for {self.cottage.name}"


def cottage_image_path(instance, filename):
    cottage_id = instance.cottage.id
    return os.path.join("cottage_images", str(cottage_id), filename)


class CottageImage(OrderedModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    cottage = models.ForeignKey(Cottage, on_delete=models.CASCADE, related_name="images", verbose_name="Коттедж")
    image = models.ImageField(upload_to=cottage_image_path, verbose_name="Фотография")

    class Meta(OrderedModel.Meta):
        verbose_name = 'Фотография коттеджа'
        verbose_name_plural = 'Фотографии коттеджа'

    def __str__(self):
        return f'Photo for {self.cottage.name}'


@receiver(pre_delete, sender=CottageImage)
def delete_cottage_image(sender, instance, **kwargs):
    instance.image.delete(False)
