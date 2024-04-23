import random
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from app_auth.utils import generate_invite_code
from app_auth.managers import UserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """ Модель пользователя """

    phone_number = models.CharField(
        max_length=15,
        unique=True,
        verbose_name='номер телефона'
    )

    invite_code = models.CharField(
        max_length=6,
        default=generate_invite_code,
        unique=True,
        verbose_name='инвайт код'
    )

    password_phone = models.CharField(
        max_length=4,
        null=True,
        verbose_name='одноразовый пароль'
    )

    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def save(self, *args, **kwargs):
        self.password_phone = random.randint(1000, 9999)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'
