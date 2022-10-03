from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models


class User(AbstractUser):
    """Модель пользователей."""
    username = models.CharField(
        unique=True,
        max_length=150,
        validators=(
            RegexValidator(
                regex=r'^[\w.@+-]+\Z',
                message='Не корректное имя пользователя'
            ),
        ),
        verbose_name='Ник пользователя',
        help_text='Укажите ник пользователя'
    )
    first_name = models.CharField(
        max_length=150,
        verbose_name='Фамилия пользователя',
        help_text='Укажите фимилию пользователя'
    )
    last_name = models.CharField(
        max_length=150,
        verbose_name='Имя пользователя',
        help_text='Укажите имя пользователя'
    )
    email = models.EmailField(
        unique=True,
        max_length=254,
        verbose_name='Email пользователя',
        help_text='Укажите email пользователя'
    )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = (
        'username',
        'first_name',
        'last_name',
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username


class Follow(models.Model):
    """Модель подписок."""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Пользователь',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Автор',
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = (
            models.UniqueConstraint(
                fields=('user', 'author'),
                name='unique_subscription',
            ),
        )

    def __str__(self):
        return f'{self.user} подписан на {self.author}'
