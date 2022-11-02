from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):

    class Role(models.IntegerChoices):
        ADMIN = 1, _("Администратор")
        MODERATOR = 2, _("Модератор")
        USER = 3, _("Пользователь")

    role = models.PositiveSmallIntegerField(
        choices=Role.choices,
        default=Role.USER,
    )

    bio = models.TextField(
        'Биография',
        blank=True
    )
