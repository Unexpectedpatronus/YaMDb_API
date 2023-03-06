from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator

from django.db import models

ROLE_CHOICES = (
    ('user', 'Пользователь'),
    ('moderator', 'Модератор'),
    ('admin', 'Администратор'),
)


class Category(models.Model):
    name = models.CharField(
        verbose_name='Название категории',
        max_length=256,
    )
    slug = models.SlugField(
        unique=True,
        verbose_name='Слаг категории',
        max_length=50,
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(
        verbose_name='Название жанра',
        max_length=256,
    )
    slug = models.SlugField(
        unique=True,
        verbose_name='Слаг жанра',
        max_length=50,
    )

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(
        verbose_name='Название произведения',
        max_length=256,
    )
    year = models.PositiveIntegerField(
        verbose_name='Год'
    )
    description = models.TextField(
        verbose_name='Описание произведения'
    )
    genre = models.ManyToManyField(
        Genre,
        verbose_name='Жанр',
        through='GenreTitle',
        related_name='titles',
        null=True
    )
    category = models.ForeignKey(
        Category,
        related_name='titles',
        on_delete=models.SET_NULL,
        verbose_name='Категория',
        null=True
    )

    class Meta:
        ordering = ('year',)
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    genre = models.ForeignKey(
        Genre,
        on_delete=models.SET_NULL,
        null=True,
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.SET_NULL,
        null=True,
    )

    class Meta:
        verbose_name = 'Связь жанра и произведения'
        verbose_name_plural = 'Связи жанров и произведений'

    def __str__(self):
        return f'{self.title} {self.genre}'


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
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        related_name='reviews',
        on_delete=models.CASCADE,
        verbose_name='Произведение'
    )
    text = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор'
    )
    score = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(10)
        ],
        verbose_name='Оценка'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'],
                name='unique_author_title')
        ]
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    def __str__(self):
        return self.text


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Отзыв'
    )
    text = models.TextField(verbose_name='Текст')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации'
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text
