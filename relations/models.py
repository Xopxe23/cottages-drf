import uuid

from django.db import models

from cottages.models import Cottage
from users.models import User


class UserCottageReview(models.Model):
    RATING_CHOICES = [
        (1, 'Очень плохо'),
        (2, 'Плохо'),
        (3, 'Нормально'),
        (4, 'Хорошо'),
        (5, 'Отлично'),
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    cottage = models.ForeignKey(Cottage, on_delete=models.CASCADE, related_name="reviews", verbose_name="Коттедж")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviews", verbose_name="Пользователь")
    location_rating = models.IntegerField(choices=RATING_CHOICES, verbose_name="Рейтинг местоположения")
    cleanliness_rating = models.IntegerField(choices=RATING_CHOICES, verbose_name="Рейтинг чистоты")
    communication_rating = models.IntegerField(choices=RATING_CHOICES, verbose_name="Рейтинг общения")
    value_rating = models.IntegerField(choices=RATING_CHOICES, verbose_name="Соотношение цена/качество")
    comment = models.TextField(verbose_name="Отзыв")
    rating = models.FloatField(blank=True, null=True, editable=False)

    def save(self, *args, **kwargs):
        ratings_sum = self.location_rating + self.cleanliness_rating + self.communication_rating + self.value_rating
        avg_rating = ratings_sum / 4.0
        self.rating = avg_rating
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Отзыв коттеджа'
        verbose_name_plural = 'Отзывы коттеджа'

    def __str__(self):
        return f'{self.cottage} - {self.user}'


class UserCottageLike(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    cottage = models.ForeignKey(Cottage, on_delete=models.CASCADE, related_name="likes", verbose_name="Коттедж")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="likes", verbose_name="Пользователь")

    class Meta:
        verbose_name = 'Понравившийся коттедж'
        verbose_name_plural = 'Понравившиеся коттеджи'

    def __str__(self):
        return f'{self.cottage} - {self.user}'


class UserCottageRent(models.Model):
    STATUS_CHOICES = [
        (1, 'Забронирован'),
        (2, 'Оплачен'),
        (3, 'Отказ'),
        (4, 'Подтвержден'),
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    cottage = models.ForeignKey(Cottage, on_delete=models.CASCADE, related_name="rents", verbose_name="Коттедж")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="rents", verbose_name="Пользователь")
    status = models.IntegerField(choices=STATUS_CHOICES, verbose_name="Статус")
    start_date = models.DateField(verbose_name="Дата заезда")
    end_date = models.DateField(verbose_name="Дата выезда")

    class Meta:
        verbose_name = 'Аренда коттеджа'
        verbose_name_plural = 'Аренды коттеджа'

    def __str__(self):
        return f'{self.cottage} - {self.user}'
