from django.urls import include, path
from recipes.views import IngredientAPIView
from rest_framework.routers import DefaultRouter


app_name = 'recipes'

router = DefaultRouter()

router.register('ingredients', IngredientAPIView)

urlpatterns = [
    path('', include(router.urls)),
]
