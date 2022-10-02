from recipes.models import Recipe
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from users.models import Follow, User


class ListUserSerializer(serializers.ModelSerializer):
    """Сериализация пользователей."""
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
        )

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if request is None or request.user.is_anonymous:
            return False
        user = request.user
        return Follow.objects.filter(user=user, author=obj).exists()


class GetRecipesFollowSerializer(serializers.ModelSerializer):
    """Серилизация рецептов при подписке на автора."""
    class Meta:
        model = Recipe
        fields = (
            'id',
            'name',
            'image',
            'cooking_time',
        )


class FollowSerializer(serializers.ModelSerializer):
    """Серилизация при добавлени / удалении подписки."""
    email = serializers.ReadOnlyField(source='author.email')
    id = serializers.ReadOnlyField(source='author.id')
    username = serializers.ReadOnlyField(source='author.username')
    first_name = serializers.ReadOnlyField(source='author.first_name')
    last_name = serializers.ReadOnlyField(source='author.last_name')
    is_subscribed = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count',
        )

        validators = [
            UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=('user', 'author')
            )
        ]

    def get_is_subscribed(self, obj):
        return Follow.objects.filter(
            user=obj.user, author=obj.author
        ).exists()

    def get_recipes(self, obj):
        queryset = obj.author.recipe.all()
        return GetRecipesFollowSerializer(queryset, many=True).data

    def get_recipes_count(self, obj):
        return obj.author.recipe.count()
