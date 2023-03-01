import datetime as dt

from rest_framework import serializers

from reviews.models import Category, Genre, GenreTitle, Title


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

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'description', 'genre', 'category')  # 'rating',

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
            raise serializers.ValidationError('Год выпуска не может быть больше текущего!')
        return value
