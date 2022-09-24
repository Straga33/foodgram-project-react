from django.urls import include, path
from rest_framework import routers

from users.views import UsersViewSet


app_name = 'users'

router = routers.DefaultRouter()

router.register('users', UsersViewSet, basename='users')

urlpatterns = [
    path('', include(router.urls)),
]
