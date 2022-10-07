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
        'is_superuser',
        'is_staff',
    )
    search_fields = (
        '^username',
        '^email',
    )
    list_filter = ('is_superuser', 'is_staff',)


class FollowAdmin(admin.ModelAdmin):
    """Админка для подписок."""
    list_display = ('user', 'author',)
    search_fields = (
        '^user__username',
        '^author__username',
    )
    list_filter = ('author',)


admin.site.register(User, UserAdmin)
admin.site.register(Follow, FollowAdmin)
