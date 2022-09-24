from django.core.exceptions import ValidationError


def validate_username(value):
    """Валидация имени на совпадение с me."""
    if value == 'me':
        raise ValidationError('Имя "me" запрещено.')
