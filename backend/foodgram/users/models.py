from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Модель User"""
    ADMIN = 'admin'
    USER = 'user'
    ADMIN_ROLE = [
        (USER, 'user'),
        (ADMIN, 'admin'),
    ]
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [
        'username',
        'first_name',
        'last_name',
    ]
    username = models.CharField(
        unique=True,
        max_length=150,
    )
    first_name = models.CharField(
        max_length=150,
    )
    last_name = models.CharField(
        max_length=150,
    )
    email = models.EmailField(
        unique=True,
        max_length=254,
        verbose_name='Email пользователя',
        help_text='Укажите email пользователя'
    )
    role = models.CharField(
        max_length=15,
        choices=ADMIN_ROLE,
        default=USER,
        verbose_name='Роль пользователя',
        help_text='Укажите роль пользователя'
    )

    class Meta:
        verbose_name = 'Пользователи'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.email
