from django.contrib import admin

from recipes.models import AmountIngredientsInRecipe, Ingredient, Recipe, Tag


class IngredientAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'measurement_unit',
    )
    list_filter = ("name",)


class TagAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'color',
        'slug',
    )
    list_filter = ('name',)


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'author')
    list_filter = (
        'name',
        'author',
        'tags',
    )


class AmountIngredientsInRecipeAdmin(admin.ModelAdmin):
    list_display = (
        'ingredient',
        'recipe',       
        'amount',
    )


admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(AmountIngredientsInRecipe, AmountIngredientsInRecipeAdmin)
