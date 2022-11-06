from django.db import models

from users.models import User
from .validators import validate_score



class Category(models.Model):
    name = models.CharField(
        verbose_name='Категория',
        max_length=200,
        help_text='Название категории'
    )
    slug = models.SlugField(
        verbose_name='Слаг',
        unique=True,
        help_text='Адрес для страницы с группой'
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(
        verbose_name='Жанр',
        max_length=200,
        help_text='Название жанра'
    )
    slug = models.SlugField(
        verbose_name='Слаг',
        unique=True,
        help_text='Адрес для страницы с жанром'
    )

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(
        verbose_name='Произведение',
        max_length=200,
        help_text='Название произведения'
    )
    year = models.IntegerField()
    category = models.ForeignKey(
        Category,
        db_column='category',
        verbose_name='Категория',
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='category',
        help_text='Категория, к которой относится произведение'
    )
    description = models.TextField(
        verbose_name='Описание',
        max_length=255,
        null=True,
        blank=True,
        help_text='Описание произведения'
    )
    genre = models.ManyToManyField(
        Genre,
        related_name='titles',
        verbose_name='Жанры',
        help_text='Жанры произведения'
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name


"""
class Reviews(models.Model):
    title_id=models.ForeignKey(Titles, on_delete=models.CASCADE, related_name='reviews')
    text=models.TextField()
    author=models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    score=models.IntegerField(validators=[validate_score])
    pub_date=models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints=[
            models.UniqueConstraint(fields=['author', 'title'], name='unique_author_title')
        ]
        ordering=('-pub_date',)

class Comments(models.Model):
    review_id=models.ForeignKey(Reviews, on_delete=models.CASCADE)
    text=models.TextField()
    author=models.ForeignKey(User, on_delete=models.CASCADE)
    pub_date=models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering=('-pub_date',)
"""
