from django.contrib import admin
from recipes.models import Ingredient
# Register your models here.

class IngredientAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'measurement_unit',
    )

admin.site.register(Ingredient, IngredientAdmin)
