from recipes.models import Ingredient, Tag
from rest_framework import serializers


class IngredientSerializer(serializers.ModelSerializer):    
    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit',)


class TagSerializer(serializers.ModelSerializer):    
    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug',)