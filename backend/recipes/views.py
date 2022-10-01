from django.db.models import Sum
from django.db.models.expressions import Exists, OuterRef
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from foodgram.settings import CONTENTTYPE, FILENAME
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import SAFE_METHODS, IsAuthenticated
from rest_framework.response import Response

from recipes.filters import IngredientFilter, RecipeFilter
from recipes.models import (AmountIngredientsInRecipe, FavoritedRecipe,
                            Ingredient, Recipe, ShoppingCart, Tag)
from recipes.permissions import IsAdminOrReadOnly, IsOwnerOrReadOnly
from recipes.serializers import (FavoriteOrShoppingRecipeSerializer,
                                 IngredientSerializer, RecipesCreateSerializer,
                                 RecipesListSerializer, TagSerializer)


class IngredientViewSet(viewsets.ModelViewSet):
    """Вьюсет для модели ингредиентов."""
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None
    filter_class = IngredientFilter
    permission_classes = (IsAdminOrReadOnly,)


class TagViewSet(viewsets.ModelViewSet):
    """Вьюсет для модели тегов."""
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None
    permission_classes = (IsAdminOrReadOnly,)


class RecipeViewSet(viewsets.ModelViewSet):
    """Вьюсет для модели рецептов.
    Добавление / удаление из избранных.
    добавление / удаление в список покупок /
    формирования и вывод списка покупок в текстовом файле."""
    queryset = Recipe.objects.all()
    permission_classes = (IsOwnerOrReadOnly,)
    filter_class = RecipeFilter

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return RecipesListSerializer
        return RecipesCreateSerializer

    def get_queryset(self):
        queryset = Recipe.objects.select_related('author').prefetch_related(
            'tags',
            'ingredients',
            'recipe',
            'shopping_cart_recipe',
            'favorite_recipe',
        )
        if self.request.user.is_authenticated:
            queryset = queryset.annotate(
                is_favorited=Exists(
                    FavoritedRecipe.objects.filter(
                        user=self.request.user, recipe=OuterRef('id')
                    )
                ),
                is_in_shopping_cart=Exists(
                    ShoppingCart.objects.filter(
                        user=self.request.user, recipe=OuterRef('id')
                    )
                ),
            )
        return queryset

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(
        methods=['POST', 'DELETE'],
        detail=True,
        permission_classes=(IsAuthenticated,),
    )
    def favorite(self, request, pk):
        recipe_pk = self.kwargs.get('pk')
        recipe = get_object_or_404(Recipe, pk=recipe_pk)
        if request.method == 'POST':
            serializer = FavoriteOrShoppingRecipeSerializer(recipe)
            FavoritedRecipe.objects.create(
                user=self.request.user,
                recipe=recipe
            )
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        elif request.method == 'DELETE':
            favorite = FavoritedRecipe.objects.filter(
                user=self.request.user,
                recipe=recipe
            )
            if favorite.exists():
                favorite.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                return Response(
                    {'errors': 'Рецепта нет в списке избранных'},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        return Response(
            {'errors': 'Недопустимая операция'},
            status=status.HTTP_400_BAD_REQUEST,
        )

    @action(
        methods=['POST', 'DELETE'],
        detail=True,
    )
    def shopping_cart(self, request, pk):
        recipe_pk = self.kwargs.get('pk')
        recipe = get_object_or_404(Recipe, pk=recipe_pk)
        if request.method == 'POST':
            serializer = FavoriteOrShoppingRecipeSerializer(recipe)
            ShoppingCart.objects.create(
                user=self.request.user,
                recipe=recipe
            )
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        elif request.method == 'DELETE':
            shopiping = ShoppingCart.objects.filter(
                user=self.request.user,
                recipe=recipe
            )
            if shopiping.exists():
                shopiping.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                return Response(
                    {'errors': 'Рецепта нет в списке покупок'},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        return Response(
            {'errors': 'Недопустимая операция'},
            status=status.HTTP_400_BAD_REQUEST,
        )

    @action(
        methods=['GET'],
        detail=False,
        permission_classes=(IsAuthenticated,),
    )
    def download_shopping_cart(self, request):
        ingredients = AmountIngredientsInRecipe.objects.select_related(
            'recipe',
            'ingredient'
        )
        ingredients = ingredients.filter(
            recipe__shopping_cart_recipe__user=request.user
        )
        ingredients = ingredients.values(
            'ingredient__name',
            'ingredient__measurement_unit'
        )
        ingredients = ingredients.annotate(ingredient_total=Sum('amount'))
        ingredients = ingredients.order_by('ingredient__name')
        shopping_list = 'Список покупок: \n'
        for ingredient in ingredients:
            shopping_list += (
                f'{ingredient["ingredient__name"]} - '
                f'{ingredient["ingredient_total"]} '
                f'({ingredient["ingredient__measurement_unit"]}) \n'
            )
            response = HttpResponse(
                shopping_list, content_type=CONTENTTYPE
            )
            response[
                'Content-Disposition'
            ] = f'attachment; filename={FILENAME}'
        return response
