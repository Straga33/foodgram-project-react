from distutils.command.upload import upload
from django.db import models
from colorfield.fields import ColorField
from users.models import User


class Ingredient(models.Model):
    """Модель ингритиета"""
    name = models.CharField(
        unique=True,
        max_length=200,
    )
    measurement_unit = models.CharField(
        unique=True,
        max_length=15,
    )

    class Meta:
        verbose_name = 'Ингредиенты'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return self.name


class Tag(models.Model):
    """Модель тега"""
    name = models.CharField(max_length=200,)
    color = ColorField(max_length=7,)
    slug = models.SlugField(max_length=150,)

    class Meta:
        verbose_name = 'Теги'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Recipe(models.Model):
    """Модель Reciept"""
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор рецепта',
        help_text='Укажите автора рецепта'
    )
    name = models.CharField(
        max_length=200,
        verbose_name='Название рецепта',
        help_text='Укажите название рецепта'
    )
    image = models.ImageField(
        upload_to='reciepe/',
        verbose_name='Картинка',
    )
    text_description = models.TextField(
        max_length=1000,
        verbose_name='Описание рецепта',
        help_text='Напишите описание рецепта'
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        related_name='recipes',
        through='AmountIngredientsInRecipe',
        verbose_name='Ингредиенты рецепта',
        help_text='Укажите ингредиенты рецепта'
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Теги рецепта',
        help_text='Укажите теги рецепта'
    )
    time_preparing = models.PositiveSmallIntegerField(
        verbose_name='Время приготовления',
        help_text='Укажите время приготовления'
    )

    class Meta:
        verbose_name = 'Рецепты'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name[:15]




