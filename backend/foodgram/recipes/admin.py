from django.contrib import admin
from recipes.models import Ingredient, Tag


class IngredientAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'measurement_unit',
    )

class TagAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'color',
        'slug',
    )

admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Tag, TagAdmin)
