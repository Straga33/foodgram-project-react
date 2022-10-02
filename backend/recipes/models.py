from django.core.validators import MinValueValidator
from django.db import models
from foodgram.settings import MINAMOUNT, MINCOOKINGTIME

from users.models import User


class Ingredient(models.Model):
    """Модель ингредиента."""
    name = models.CharField(
        unique=True,
        max_length=200,
        verbose_name='Название ингредиента',
        help_text='Укажите название ингредиента'
    )
    measurement_unit = models.CharField(
        max_length=200,
        verbose_name='Еденица измерения',
        help_text='Укажите единицу измерения'
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return self.name


class Tag(models.Model):
    """Модель тега."""
    name = models.CharField(
        max_length=200,
        verbose_name='Название тега',
        help_text='Укажите название тега',
    )
    color = models.CharField(
        max_length=7,
        verbose_name='Цвет тега',
        help_text='Укажите цвет тега',
    )
    slug = models.SlugField(
        max_length=200,
        verbose_name='Слаг тега',
        help_text='Укажите слаг тега',
    )

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Recipe(models.Model):
    """Модель рецепта."""
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipe',
        verbose_name='Автор рецепта',
        help_text='Укажите автора рецепта'
    )
    name = models.CharField(
        max_length=200,
        verbose_name='Название рецепта',
        help_text='Укажите название рецепта'
    )
    image = models.ImageField(
        upload_to='recipes_images/',
        verbose_name='Картинка рецепта',
    )
    text = models.TextField(
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
        related_name='recipe',
        verbose_name='Теги рецепта',
        help_text='Укажите теги рецепта',
    )
    cooking_time = models.PositiveSmallIntegerField(
        validators=(
            MinValueValidator(
                MINCOOKINGTIME,
                message='Минимальное время приготовления 1 минута'
            ),
        ),
        verbose_name='Время приготовления',
        help_text='Укажите время приготовления'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации',
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name[:15]


class AmountIngredientsInRecipe(models.Model):
    """Модель количества ингредиентов в рецепте."""
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='ingredient',
        verbose_name='Ингредиент',
        help_text='Укажите ингредиент'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='recipe',
        verbose_name='Рецепт',
        help_text='Укажите рецепт'
    )
    amount = models.PositiveSmallIntegerField(
        validators=(
            MinValueValidator(
                MINAMOUNT, message='Минимум 1 единица ингредиента'
            ),
        ),
        verbose_name='Количество ингредиента',
        help_text='Укажите количество ингредиента'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=('recipe', 'ingredient'),
                name='unique_ingredient',
            )
        ]
        verbose_name = 'Количество ингредиента'
        verbose_name_plural = 'Количество ингредиентов'

    def __str__(self):
        return f'{self.ingredient} {self.amount}'


class FavoritedRecipe(models.Model):
    """Модель для выбора любимого рецепта."""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorited_user',
        verbose_name='Пользователь',
    )

    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorite_recipe',
        verbose_name='Избранный рецепт',
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'recipe'),
                name='unique_favorited',
            )
        ]
        verbose_name = 'Избранный рецепт'
        verbose_name_plural = 'Избранные рецепты'

    def __str__(self):
        return f'{self.user} любит {self.recipe}'


class ShoppingCart(models.Model):
    """Модель листа покупок."""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shopping_cart_user',
        verbose_name='Пользователь',
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='shopping_cart_recipe',
        verbose_name='Рецепт',
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'recipe'),
                name='unique_recipe_in_shopping_cart',
            )
        ]
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Списки покупок'

    def __str__(self):
        return f'{self.user} добавил {self.recipe}'
