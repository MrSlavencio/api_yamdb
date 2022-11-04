from enum import Enum

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class RoleChoice(Enum):
    ADMIN = "admin"
    MODERATOR = "moderator"
    USER = "user"

    @classmethod
    def choices(cls):
        return tuple((c.name, c.value) for c in cls)


class User(AbstractUser):
    email = models.EmailField(_('email address'), unique=True,)
    role = models.TextField(
        choices=RoleChoice.choices(),
        default=RoleChoice.USER,
    )
    bio = models.TextField(
        _('Биография'),
        blank=True
    )
    REQUIRED_FIELDS = ["email", ]
