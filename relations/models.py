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
    cottage_rating = models.IntegerField(choices=RATING_CHOICES, verbose_name="Рейтинг коттеджа")
    cleanliness_rating = models.IntegerField(choices=RATING_CHOICES, verbose_name="Рейтинг чистоты")
    owner_rating = models.IntegerField(choices=RATING_CHOICES, verbose_name="Рейтинг хозяина")
    comment = models.TextField(verbose_name="Отзыв")

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
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    cottage = models.ForeignKey(Cottage, on_delete=models.CASCADE, related_name="rents", verbose_name="Коттедж")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="rents", verbose_name="Пользователь")
    start_date = models.DateField(verbose_name="Дата заезда")
    end_date = models.DateField(verbose_name="Дата выезда")

    class Meta:
        verbose_name = 'Аренда коттеджа'
        verbose_name_plural = 'Аренды коттеджа'

    def __str__(self):
        return f'{self.cottage} - {self.user}'
