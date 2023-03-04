import csv

from reviews.models import Category, Genre, GenreTitle, Title


def run():
    with open('static/data/category.csv', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)

        Title.objects.all().delete()
        Category.objects.all().delete()
        Genre.objects.all().delete()

        for row in reader:
            print(row)

            category = Category(
                id=row[0],
                name=row[1],
                slug=row[2],
            )
            category.save()

    with open('static/data/genre.csv', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)

        for row in reader:
            print(row)

            genre = Genre(
                id=row[0],
                name=row[1],
                slug=row[2],
            )
            genre.save()

    with open('static/data/titles.csv', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)

        for row in reader:
            print(row)

            category, _ = Category.objects.get_or_create(id=row[3])

            title = Title(
                id=row[0],
                name=row[1],
                year=row[2],
                category=category,
            )
            title.save()

    with open('static/data/genre_title.csv', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)

        for row in reader:
            print(row)

            genre, _ = Genre.objects.get_or_create(id=row[2])
            title, _ = Title.objects.get_or_create(id=row[1])

            genre_title = GenreTitle(
                id=row[0],
                genre=genre,
                title=title,
            )
            genre_title.save()
