import csv

from reviews.models import (Category, Comment, Genre, GenreTitle, Review,
                            Title, User)


def run():
    with open('static/data/users.csv', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)

        Title.objects.all().delete()
        Category.objects.all().delete()
        Genre.objects.all().delete()
        User.objects.all().delete()
        GenreTitle.objects.all().delete()
        Review.objects.all().delete()
        Comment.objects.all().delete()

        for row in reader:
            print(row)

            user = User(
                id=row[0],
                username=row[1],
                email=row[2],
                role=row[3],
                bio=row[4],
            )
            user.save()

    with open('static/data/category.csv', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)

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

    with open('static/data/review.csv', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)

        for row in reader:
            print(row)

            author, _ = User.objects.get_or_create(id=row[3])
            title, _ = Title.objects.get_or_create(id=row[1])

            review = Review(
                id=row[0],
                title=title,
                text=row[2],
                author=author,
                score=row[4],
                pub_date=row[5]
            )
            review.save()

    with open('static/data/comments.csv', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)

        for row in reader:
            print(row)

            author, _ = User.objects.get_or_create(id=row[3])
            review, _ = Review.objects.get_or_create(id=row[1])

            comment = Comment(
                id=row[0],
                review=review,
                text=row[2],
                author=author,
                pub_date=row[4],
            )
            comment.save()
