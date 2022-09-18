from django.shortcuts import render
from recipes.serializer import IngredientSerializer
from recipes.models import Ingredient
from rest_framework import viewsets


class IngredientAPIView(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
