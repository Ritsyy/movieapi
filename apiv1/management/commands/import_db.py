from django.core.management.base import BaseCommand

import json
import csv
import os
from django.conf import settings
from apiv1.models import Genre, Movie
from apiv1.serializers import MovieSerializer


class Command(BaseCommand):

    def handle(self, *args, **options):
        path = os.path.join(settings.BASE_DIR, 'apiv1/data/movies.json')
        data = json.load(open(path))

        for movie_data in data:
            obj = {}
            obj['popularity'] = movie_data.get('99popularity')
            obj['director'] = movie_data.get('director')
            obj['score'] = movie_data.get('imdb_score')
            obj['name'] = movie_data.get('name')
            new_movie, created = Movie.objects.get_or_create(**obj)
            for genre in movie_data.get('genre'):
                genre = genre.strip()
                new_genre, created = Genre.objects.get_or_create(name=genre)
                new_movie.genre.add(new_genre)
                new_movie.save()
