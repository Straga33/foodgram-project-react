from django_filters.rest_framework import FilterSet, filters

from recipes.models import Ingredient, Recipe


class RecipeFilter(FilterSet):
    """Фильтр рецептов."""
    is_favorited = filters.BooleanFilter(
        method='get_favorited'
    )
    author = filters.AllValuesFilter(
        field_name='author'
    )
    is_in_shopping_cart = filters.BooleanFilter(
        method='get_in_shopping_cart'
    )
    tags = filters.AllValuesMultipleFilter(
        field_name='tags__slug'
    )

    def get_favorited(self, queryset, name, data):
        if data and not self.request.user.is_anonymous:
            return queryset.filter(favorite_recipe__user=self.request.user)
        return queryset

    def get_in_shopping_cart(self, queryset, name, data):
        if data and not self.request.user.is_anonymous:
            return queryset.filter(
                shopping_cart_recipe__user=self.request.user
            )
        return queryset

    class Meta:
        model = Recipe
        fields = [
            'is_favorited',
            'author',
            'is_in_shopping_cart',
            'tags',
        ]


class IngredientFilter(FilterSet):
    """Фильтр ингредиентов."""
    name = filters.CharFilter(
        lookup_expr='istartswith',
    )

    class Meta:
        model = Ingredient
        fields = ['name', ]
