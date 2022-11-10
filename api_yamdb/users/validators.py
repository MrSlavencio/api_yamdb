from django.core.exceptions import ValidationError


def username_not_me_validator(value):
    if value == 'me':
        raise ValidationError(
            ('Имя пользователя не может быть "me".'),
            params={'value': value},
        )
