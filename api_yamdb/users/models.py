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
    username = models.CharField(
        _('Имя пользователя'),
        max_length=150,
        unique=True,
        help_text=_("""Обязательное поле. 150 символов или меньше.
        Только буквы, цифры или символы @/./+/-/_"""),
        validators=[AbstractUser.username_validator],
        error_messages={
            'unique': _("Пользователь с таким именем уже существует"),
        },
    )
    email = models.EmailField(
        _('Адрес электронной почты'),
        unique=True,
        max_length=254,)
    first_name = models.CharField(_('Имя'), max_length=150, blank=True)
    last_name = models.CharField(_('Фамилия'), max_length=150, blank=True)
    role = models.TextField(
        choices=RoleChoice.choices(),
        default=RoleChoice.USER,
    )
    bio = models.TextField(
        _('Биография'),
        blank=True
    )
    REQUIRED_FIELDS = ["email", ]

    @property
    def is_user(self):
        return self.role == RoleChoice.USER

    @property
    def is_admin(self):
        return self.role == RoleChoice.ADMIN

    @property
    def is_moderator(self):
        return self.role == RoleChoice.MODERATOR

    class Meta:
        ordering = ("id", )
        verbose_name = _('Пользователь')
        verbose_name_plural = _('Пользователи')

    def __str__(self):
        return self.username
