from datetime import datetime
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator


def validate_score(value):
    if value not in range(1, 11):
        raise ValidationError(
            'Значение оценки должно быть в диапозоне от 1 до 10'
        )


def year_validator(value):
    if value not in range(1930, datetime.now().year + 1):
        raise ValidationError(
            f'Год произведения должен быть с 1930 по {datetime.now().year}'
        )


slug_validator = RegexValidator(
    r'[a-z0-9_\-]',
    message='Некорректное значение поля Slug'
)
