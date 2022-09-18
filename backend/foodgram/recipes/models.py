from django.db import models

# Create your models here.
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
