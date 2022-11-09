from django.contrib.auth.models import AbstractUser
from django.contrib.auth.tokens import default_token_generator as tok_gen
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _

from .validators import username_not_me_validator

CONFIRMATION_CODE_LENGTH = 255


class User(AbstractUser):
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'

    ROLE_CHOICES = (
        (USER, 'Пользователь'),
        (MODERATOR, 'Модератор'),
        (ADMIN, 'Администратор'),
    )
    MAX_ROLE_LENGTH = max(len(c) for c, _ in ROLE_CHOICES)

    username = models.CharField(
        _('Имя пользователя'),
        max_length=150,
        unique=True,
        help_text=_("""Обязательное поле. 150 символов или меньше.
        Только буквы, цифры или символы @/./+/-/_"""),
        validators=[AbstractUser.username_validator,
                    username_not_me_validator, ],
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
    role = models.CharField(
        max_length=MAX_ROLE_LENGTH,
        choices=ROLE_CHOICES,
        default=USER,
    )
    bio = models.TextField(
        _('Биография'),
        blank=True,
    )
    confirmation_code = models.CharField(
        'Код подтверждения',
        max_length=CONFIRMATION_CODE_LENGTH,
        blank=True,
    )

    REQUIRED_FIELDS = ["email", ]

    class Meta:
        ordering = ("id", )
        verbose_name = _('Пользователь')
        verbose_name_plural = _('Пользователи')

    def save(self, *args, **kwargs):
        if self.is_admin:
            self.is_staff = True
        super(User, self).save(*args, **kwargs)

    def __str__(self):
        return self.username

    @ property
    def is_user(self):
        return self.role == self.USER

    @ property
    def is_admin(self):
        return self.role == self.ADMIN

    @ property
    def is_moderator(self):
        return self.role == self.MODERATOR


@receiver(post_save, sender=User)
def user_created(sender, instance, created, **kwargs):
    if created:
        confirmation_code = tok_gen.make_token(instance)
        instance.confirmation_code = confirmation_code
        instance.save()
