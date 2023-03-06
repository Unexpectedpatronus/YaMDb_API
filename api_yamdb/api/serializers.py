import datetime as dt
from django.db.models import Avg

from rest_framework import serializers

from reviews.models import (ROLE_CHOICES, Category, Genre, GenreTitle, Title,
                            User, Review, Comment)


class UserSerializer(serializers.ModelSerializer):
    role = serializers.ChoiceField(choices=ROLE_CHOICES)

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('name', 'slug')


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'slug')


class TitleSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True, required=True)
    rating = serializers.SerializerMethodField()
    category = CategorySerializer()
    description = serializers.CharField(required=False)

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'rating', 'description', 'genre', 'category'
        )

    def get_rating(self, obj):
        result = Title.objects.aggregate(rating=Avg('reviews__score'))
        return result['rating']

    def create(self, validated_data):
        if 'genre' not in self.initial_data:
            title = Title.objects.create(**validated_data)
            return title

        genre = validated_data.pop('genre')
        title = Title.objects.create(**validated_data)
        for element in genre:
            current_genre, status = Genre.objects.get_or_create(
                **element)
            GenreTitle.objects.create(
                genre=current_genre, title=title)
        return title

    def validate_year(self, value):
        if value > dt.date.today().year:
            raise serializers.ValidationError(
                'Год выпуска не может быть больше текущего!'
            )
        return value


class SignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email')

    def validate_username(self, value):
        if value.lower() == 'me':
            raise serializers.ValidationError(
                'Имя пользователя "me" не разрешено.'
            )
        return value


class TokenSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('username', 'confirmation_code')


class ReviewSerializer(serializers.ModelSerializer):
     text = serializers.CharField(required=True)
     score = serializers.IntegerField(required=True)

     class Meta:
         model = Review
         fields = ('id', 'text', 'author', 'score', 'pub_date')


class CommentSerializer(serializers.ModelSerializer):
     text = serializers.CharField(required=True)

     class Meta:
         model = Comment
         fields = ('id', 'text', 'author', 'pub_date')
