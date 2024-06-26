import datetime
import random
import string
import uuid

from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.validators import RegexValidator
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True, db_index=True)
    phone_number = models.CharField(unique=True, max_length=10, null=True, validators=[
        RegexValidator(r'^\d{10}$', message='Phone number must be exactly 10 digits.')
    ], verbose_name="Номер телефона")
    first_name = models.CharField(max_length=30, blank=True, verbose_name="Имя")
    last_name = models.CharField(max_length=30, blank=True, verbose_name="Фамилия")
    photo = models.ImageField(blank=True, null=True, verbose_name="Фото")
    is_active = models.BooleanField(default=True, verbose_name="Активен")
    is_rentier = models.BooleanField(default=False, verbose_name="Арендодатель")
    is_staff = models.BooleanField(default=False, verbose_name="Сотрудник")

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class VerifyCodeManager(models.Manager):

    def create_verify_code(self, user: User) -> "VerifyCode":
        code = self.model(user=user)
        code.save()
        return code

    def delete_verification_codes_for_user(self, user: User) -> None:
        self.filter(user=user).delete()


class VerifyCode(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code = models.CharField(max_length=6)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    expires_at = models.DateTimeField()

    objects = VerifyCodeManager()

    def save(self, *args, **kwargs) -> None:
        self.code = self.generate_verify_code()
        self.expires_at = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=5)
        super().save(*args, **kwargs)

    @staticmethod
    def generate_verify_code() -> str:
        """
        Generates a random code consisting of 6 uppercase Latin letters.
        :return: String containing the generated code.
        """
        return ''.join(random.choices(string.ascii_uppercase, k=6))

    def __str__(self) -> str:
        return f"Verification code for {self.user}"
