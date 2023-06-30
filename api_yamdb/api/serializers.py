import datetime as dt

from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.validators import UniqueTogetherValidator
from reviews.models import Category, Comment, Genre, Review, Title, User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role')
        model = User
        lookup_field = 'username'
        extra_kwargs = {
            'url': {'lookup_field': 'username'}
        }

    def validate_username(self, username):
        if username == 'me':
            raise serializers.ValidationError('Имя me не допустимо')
        if not username:
            raise serializers.ValidationError('Заполните поле имя')
        return username

    def validate_email(self, email):
        if not email:
            raise serializers.ValidationError('Заполните поле email')
        return email


class AuthentificationSerializer(serializers.Serializer):
    username = serializers.RegexField(
        max_length=150,
        regex=r"^[\w.@+-]+\Z",
        required=True
    )
    email = serializers.EmailField(
        max_length=254,
        required=True
    )

    def validate_username(self, value):
        if value.lower() == 'me':
            raise serializers.ValidationError('Имя "me" запрещено.')
        return value

    def validate(self, data):
        if User.objects.filter(username=data.get('username'),
                               email=data.get('email')).exists():
            return data
        if User.objects.filter(username=data.get('username')).exists():
            raise serializers.ValidationError(
                f'Пользователь с таким именем {data} уже существует.'
            )
        if User.objects.filter(email=data.get('email')).exists():
            raise serializers.ValidationError(
                f'Пользователь с таким email: {data} уже существует.'
            )
        return data


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150, required=True)
    confirmation_code = serializers.CharField(max_length=100, required=True)


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('name', 'slug')
        lookup_field = 'slug'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'slug')
        lookup_field = 'slug'


class TitleListSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True)
    rating = serializers.IntegerField()
    category = CategorySerializer()
    description = serializers.CharField(required=False)

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'rating', 'description', 'genre', 'category'
        )


class TitlePostSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='slug', many=True,
    )
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug',
    )
    description = serializers.CharField(
        required=False
    )

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'description', 'genre', 'category'
        )

    def validate_year(self, value):
        if value > dt.date.today().year:
            raise serializers.ValidationError(
                'Год выпуска не может быть больше текущего!'
            )
        return value


class ReviewSerializer(serializers.ModelSerializer):
    text = serializers.CharField(required=True)
    score = serializers.IntegerField(required=True)
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True,
        default=serializers.CurrentUserDefault()
    )
    title = serializers.HiddenField(default=Title.objects.all())

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date', 'title')
        validators = [
            UniqueTogetherValidator(
                queryset=Review.objects.all(),
                fields=('title', 'author'),
                message='Отзыв уже оставлен'
            )
        ]

    def validate(self, data):
        request = self.context['request']
        if request.method != 'POST':
            return data
        author = request.user
        title_id = self.context['request'].parser_context['kwargs']['title_id']
        if Review.objects.filter(title_id=title_id, author=author).exists():
            raise ValidationError(
                'Можно оставить только один отзыв на произведение.'
            )
        return data

    def validate_score(self, value):
        if not 1 <= value <= 10:
            raise serializers.ValidationError(
                'Ваша оценка должна быть в диапазоне от 1 до 10.'
            )
        return value


class CommentSerializer(serializers.ModelSerializer):
    text = serializers.CharField(required=True)
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True
    )

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')
