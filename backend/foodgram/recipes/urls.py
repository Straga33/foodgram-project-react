from django.urls import include, path
from recipes.views import IngredientAPIView, TagAPIView
from rest_framework.routers import DefaultRouter


app_name = 'recipes'

router = DefaultRouter()

router.register('ingredients', IngredientAPIView)
router.register('tags', TagAPIView)

urlpatterns = [
    path('', include(router.urls)),
]
