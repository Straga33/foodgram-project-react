from django.shortcuts import render
from recipes.serializer import IngredientSerializer, TagSerializer
from recipes.models import Ingredient, Tag
from rest_framework import viewsets


class IngredientAPIView(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer


class TagAPIView(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


# class RecieptAPIView()
