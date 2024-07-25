import os
import uuid
from typing import Union

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import Avg, ExpressionWrapper, FloatField, Q
from django.db.models.functions import Coalesce, Round
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from ordered_model.models import OrderedModel

from relations.models import UserCottageRent
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


class CottageManager(models.Manager):

    def get_cottages_list(self, start_date: str = None, end_date: str = None) -> models.QuerySet:
        """Return cottages with annotated rating"""
        cottages = self.filter(is_ready=True).select_related("category", "town").prefetch_related(
            "images", "reviews").annotate(
            average_rating=Coalesce(ExpressionWrapper(Round(Avg("reviews__rating"), 1),
                                                      output_field=FloatField()), 0.0)
        )
        if start_date and end_date:
            booked_cottages_ids = self._get_booked_cottages_ids(start_date, end_date)
            cottages = cottages.exclude(id__in=booked_cottages_ids)
        return cottages

    def get_cottage_by_id(self, id: uuid.UUID) -> Union["Cottage", None]:
        """Return cottage by ID"""
        cottage = self.filter(id=id).select_related("town", "category", "owner").prefetch_related("images").annotate(
            average_rating=Coalesce(Avg("reviews__rating"), 0.0),
            average_location_rating=Coalesce(Avg("reviews__location_rating"), 0.0),
            average_cleanliness_rating=Coalesce(Avg("reviews__cleanliness_rating"), 0.0),
            average_communication_rating=Coalesce(Avg("reviews__communication_rating"), 0.0),
            average_value_rating=Coalesce(Avg("reviews__value_rating"), 0.0)
        ).first()
        return cottage

    # noinspection PyMethodMayBeStatic
    def _get_booked_cottages_ids(self, start_date: str, end_date: str) -> list[uuid.UUID]:
        """Return id's of booked cottages on current dates"""
        booked_cottages_ids = UserCottageRent.objects.filter(
            Q(start_date__gte=start_date, start_date__lt=end_date) |
            Q(start_date__lte=start_date, end_date__gt=start_date)
        ).exclude(status=3).values_list('cottage')
        return booked_cottages_ids


class Cottage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    category = models.ForeignKey(CottageCategory, on_delete=models.CASCADE, verbose_name="Категория")  # основное
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")  # основное
    name = models.CharField(max_length=255, verbose_name="Название", blank=True, null=True)  # основное
    description = models.TextField(verbose_name="Описание", blank=True, null=True)  # основное
    town = models.ForeignKey(Town, on_delete=models.CASCADE, verbose_name="Населенный пункт", blank=True, null=True)
    address = models.CharField(max_length=255, null=True, blank=True, verbose_name="Адрес")
    latitude = models.FloatField(validators=[MinValueValidator(-90), MaxValueValidator(90)], verbose_name="Широта",
                                 blank=True, null=True)
    longitude = models.FloatField(validators=[MinValueValidator(-180), MaxValueValidator(180)], verbose_name="Долгота",
                                  blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена", blank=True, null=True)
    guests = models.PositiveIntegerField(validators=[MaxValueValidator(50)], verbose_name="Кол-во гостей",
                                         blank=True, null=True)
    beds = models.PositiveIntegerField(validators=[MaxValueValidator(30)], verbose_name="Кол-во кроватей",
                                       blank=True, null=True)
    rooms = models.PositiveIntegerField(validators=[MaxValueValidator(15)], verbose_name="Кол-во комнат",
                                        blank=True, null=True)
    total_area = models.PositiveIntegerField(validators=[MaxValueValidator(500)], verbose_name="Общая площадь",
                                             blank=True, null=True)
    parking_places = models.PositiveIntegerField(default=0, verbose_name="Кол-во парковочных мест",
                                                 blank=True, null=True)
    check_in_time = models.TimeField(verbose_name="Время заезда", blank=True, null=True)
    check_out_time = models.TimeField(verbose_name="Время выезда", blank=True, null=True)
    rules = models.JSONField(verbose_name="Правила", blank=True, null=True)
    amenities = models.JSONField(verbose_name="Условия", blank=True, null=True)
    is_ready = models.BooleanField(default=False)

    objects = CottageManager()

    class Meta:
        verbose_name = 'Коттедж'
        verbose_name_plural = 'Коттеджи'

    def __str__(self):
        return f'{self.name} in {self.town.name}'

    def is_available(self, start_date: str, end_date: str):
        """Return True if cottage is available else False"""
        existing_rents = self.rents.exclude(status=3)
        is_available = not existing_rents.filter(
            Q(start_date__gte=start_date, start_date__lt=end_date) |
            Q(start_date__lte=start_date, end_date__gt=start_date)
        ).exists()

        return is_available


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
