from django.contrib import admin

from users.models import Follow, User


class UserAdmin(admin.ModelAdmin):
    """Админка для пользователей."""
    list_display = (
        'id',
        'username',
        'email',
        'first_name',
        'last_name',
    )
    search_fields = ('username', 'email',)
    list_filter = ('username', 'email',)


class FollowAdmin(admin.ModelAdmin):
    """Админка для подписок."""
    list_display = ('user', 'author',)
    search_fields = ('user', 'author',)
    list_filter = ('author',)


admin.site.register(User, UserAdmin)
admin.site.register(Follow, FollowAdmin)
