from django.shortcuts import render
from recipes.serializer import IngredientSerializer, TagSerializer, RecipeSerializer
from recipes.models import Ingredient, Tag, Recipe
from rest_framework import viewsets


class IngredientAPIView(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer


class TagAPIView(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class RecipeAPIView(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
