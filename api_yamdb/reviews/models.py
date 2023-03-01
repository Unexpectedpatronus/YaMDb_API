from django.db import models
from django.contrib.auth.models import AbstractUser


ROLE_CHOICES = (
    ('user', 'Пользователь'),
    ('moderator', 'Модератор'),
    ('admin', 'Администратор'),
)

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


class User(AbstractUser):
    email = models.EmailField(
        unique=True,
        verbose_name='Адрес электронной почты'
    )
    role = models.CharField(
        max_length=255,
        choices=ROLE_CHOICES,
        default='user',
        verbose_name='Роль'
    )
    bio = models.TextField(
        blank=True,
        verbose_name='Биография'
    )

    class Meta:
        verbose_name = 'Пользователь'

    def __str__(self) -> str:
        return self.username
