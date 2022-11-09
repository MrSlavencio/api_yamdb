from django.core.exceptions import ValidationError

def validate_score(value):
    if value not in range(1,11):
        raise ValidationError('Значение оценки должно быть в диапозоне от 1 до 10')