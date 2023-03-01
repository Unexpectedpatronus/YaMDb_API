from django.db import models


class Category(models.Model):
    name = models.CharField(
        'Название категории',
        max_length=256,
    )
    slug = models.SlugField(
        unique=True,
        max_length=50,
    )


class Genre(models.Model):
    name = models.CharField(
        'Название жанра',
        max_length=256,
    )
    slug = models.SlugField(
        unique=True,
        max_length=50,
    )


class Title(models.Model):
    name = models.CharField(
        'Название роизведения',
        max_length=256,
    )
    year = models.IntegerField()
    description = models.TextField('Описание произведения')
    genre = models.ManyToManyField(
        Genre,
        through='GenreTitle',
    )
    category = models.ForeignKey(
        Category,
        related_name='titles',
        on_delete=models.CASCADE,
        blank=True, null=True,
        verbose_name='Категория',
    )


class GenreTitle(models.Model):
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    title = models.ForeignKey(Title, on_delete=models.CASCADE)
