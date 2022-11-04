from django.db import models


class Categories(models.Model):
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


class Titles(models.Model):
    name = models.CharField(
        verbose_name='Произведение',
        max_length=200,
        help_text='Название произведения'
    )
    year = models.IntegerField()
    category = models.ForeignKey(
        Categories,
        db_column='category',
        verbose_name='Категория',
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='category',
        help_text='Категория, к которой относится произведение'
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name


class Genres(models.Model):
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


class GenreTitle(models.Model):
    title_id=models.ForeignKey(
        Titles,
        db_column='title_id',
        verbose_name='Произведение',
        on_delete=models.CASCADE,
        related_name='title',
        help_text='Произведение определенного жанра'
    )
    genre_id=models.ForeignKey(
        Genres,
        db_column='genre_id',
        verbose_name='Жанр',
        on_delete=models.CASCADE,
        related_name='genre',
        help_text='Жанр произведения'
    )
    
    def __str__(self):
        return self.title_id.name + '&' + self.genre_id.name
