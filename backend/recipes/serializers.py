from django.db import transaction
from drf_extra_fields.fields import Base64ImageField
from foodgram.settings import MINAMOUNT, MINCOOKINGTIME
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from users.serializers import ListUserSerializer

from recipes.models import (AmountIngredientsInRecipe, FavoritedRecipe,
                            Ingredient, Recipe, ShoppingCart, Tag)


class IngredientSerializer(serializers.ModelSerializer):
    """Сериализация игнредиентов."""
    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit',)


class TagSerializer(serializers.ModelSerializer):
    """Сериализация тегов."""
    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug',)


class AmountIngredientSerializer(serializers.ModelSerializer):
    """Сериализация количества ингредиентов в рецепте."""
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = AmountIngredientsInRecipe
        fields = (
            'id',
            'name',
            'measurement_unit',
            'amount',
        )

        validators = (
            UniqueTogetherValidator(
                queryset=AmountIngredientsInRecipe.objects.all(),
                fields=('recipe', 'ingredient',)
            ),
        )


class AddAmountIngredientSerializer(serializers.ModelSerializer):
    """Сериализация количества ингредиентов при добавлении в рецепт."""
    id = serializers.PrimaryKeyRelatedField(queryset=Ingredient.objects.all())
    amount = serializers.IntegerField()

    class Meta:
        model = AmountIngredientsInRecipe
        fields = (
            'id',
            'amount',
        )


class RecipesListSerializer(serializers.ModelSerializer):
    """Сериализация рецепта."""
    tags = TagSerializer(many=True)
    author = ListUserSerializer(
        read_only=True, default=serializers.CurrentUserDefault()
    )
    ingredients = AmountIngredientSerializer(
        many=True, required=True, source='recipe'
    )
    is_favorited = serializers.BooleanField(read_only=True)
    is_in_shopping_cart = serializers.BooleanField(read_only=True)
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time',
        )


class RecipesCreateSerializer(serializers.ModelSerializer):
    """Сериализация при создании рецепта."""
    ingredients = AddAmountIngredientSerializer(many=True)
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(), many=True
    )
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = '__all__'
        read_only_fields = ('author',)

    def validate(self, data):
        cooking_time = int(self.initial_data['cooking_time'])
        amount = data['ingredients'][0]['amount']
        if cooking_time < MINCOOKINGTIME:
            raise serializers.ValidationError({
                'cooking_time': f'Минимум {MINCOOKINGTIME} минут(а).'
            })
        if amount < MINAMOUNT:
            raise serializers.ValidationError({
                'amount': f'Минимум {MINAMOUNT} единиц(а) ингредиента.'
            })
        ingredients = data['ingredients']
        unique_set = set()
        for ingredient_data in ingredients:
            current_ingredient = ingredient_data['id']
            if current_ingredient in unique_set:
                raise serializers.ValidationError(
                    'Уберите повторяющиеся ингредиенты из состава.'
                )
            unique_set.add(current_ingredient)
        return data

    def create_amount_ingredients(self, ingredients, recipe):
        for ingredient in ingredients:
            AmountIngredientsInRecipe.objects.create(
                recipe=recipe,
                ingredient=ingredient.get('id'),
                amount=ingredient.get('amount'),
            )

    @transaction.atomic
    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        recipe = super().create(validated_data)
        recipe.tags.set(tags)
        self.create_amount_ingredients(ingredients, recipe)
        return recipe

    @transaction.atomic
    def update(self, obj, validated_data):
        if 'ingredients' in validated_data:
            ingredients = validated_data.pop('ingredients')
            obj.ingredients.clear()
            self.create_amount_ingredients(ingredients, obj)
        if 'tags' in validated_data:
            tags = validated_data.pop('tags')
            obj.tags.set(tags)
        return super().update(obj, validated_data)

    def to_representation(self, instance):
        serializer = RecipesListSerializer(instance)
        return serializer.data


class FavoriteRecipeSerializer(serializers.ModelSerializer):
    """Сериализация при добавлении в список избранных."""
    class Meta:
        model = Recipe
        fields = (
            'id',
            'name',
            'image',
            'cooking_time',
        )

        validators = (
            UniqueTogetherValidator(
                queryset=FavoritedRecipe.objects.all(),
                fields=('user', 'recipe')
            ),
        )


class ShoppingRecipeSerializer(serializers.ModelSerializer):
    """Сериализация при добавлении в список покупок ."""
    class Meta:
        model = Recipe
        fields = (
            'id',
            'name',
            'image',
            'cooking_time',
        )

        validators = (
            UniqueTogetherValidator(
                queryset=ShoppingCart.objects.all(),
                fields=('user', 'recipe')
            ),
        )
