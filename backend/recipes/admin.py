from django.contrib import admin

from recipes.models import AmountIngredientsInRecipe, Ingredient, Recipe, Tag


class IngredientAdmin(admin.ModelAdmin):
    """Админка для ингредиентов."""
    list_display = (
        'id',
        'name',
        'measurement_unit',
    )
    list_filter = ("name",)


class TagAdmin(admin.ModelAdmin):
    """Админка для тегов."""
    list_display = (
        'id',
        'name',
        'color',
        'slug',
    )
    list_filter = ('name',)


class RecipeAdmin(admin.ModelAdmin):
    """Админка для рецептов."""
    list_filter = (
        'name',
        'author',
        'tags',
    )
    list_display = (
        'name',
        'author',
        'amount_in_favorites',
    )


    def amount_in_favorites(self, obj):
        return obj.favorite_recipe.count()
    amount_in_favorites.short_description = 'Количество добавлений в избранное'


class AmountIngredientsInRecipeAdmin(admin.ModelAdmin):
    """Админка для количества ингредиентов в рецептах."""
    list_display = (
        'ingredient',
        'recipe',
        'amount',
    )


admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(AmountIngredientsInRecipe, AmountIngredientsInRecipeAdmin)
