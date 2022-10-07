from django.contrib import admin

from recipes.models import (AmountIngredientsInRecipe, FavoritedRecipe,
                            Ingredient, Recipe, ShoppingCart, Tag)


class IngredientAdmin(admin.ModelAdmin):
    """Админка для ингредиентов."""
    list_display = (
        'name',
        'measurement_unit',
    )
    search_fields = ('^name',)
    list_filter = ('measurement_unit',)


class TagAdmin(admin.ModelAdmin):
    """Админка для тегов."""
    list_display = (
        'id',
        'name',
        'color',
        'slug',
    )
    list_filter = ('name',)


class IngredientInline(admin.TabularInline):
    model = AmountIngredientsInRecipe
    extra = 1


class RecipeAdmin(admin.ModelAdmin):
    """Админка для рецептов."""
    inlines = (
        IngredientInline,
    )
    list_display = (
        'id',
        'name',
        'author',
        'amount_in_favorites',
    )
    list_filter = (
        'tags',
    )
    search_fields = (
        '^name',
        '^author__username',
        '^author__email',
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
    search_fields = (
        '^ingredient__name',
        '^recipe__name',
    )
    list_filter = ('recipe__tags',)


class FavoritedRecipeAdmin(admin.ModelAdmin):
    """Админка для избранных рецептов."""
    list_display = (
        'user',
        'recipe',
    )
    search_fields = (
        '^recipe__name',
        '^user__username',
        '^user__email',
    )
    list_filter = ('recipe__tags',)


class ShoppingCartAdmin(admin.ModelAdmin):
    """Админка для листа покупок (корзина)."""
    list_display = (
        'user',
        'recipe',
    )
    search_fields = (
        '^recipe__name',
        '^user__username',
        '^user__email',
    )
    list_filter = ('recipe__tags',)


admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(AmountIngredientsInRecipe, AmountIngredientsInRecipeAdmin)
admin.site.register(FavoritedRecipe, FavoritedRecipeAdmin)
admin.site.register(ShoppingCart, ShoppingCartAdmin)
