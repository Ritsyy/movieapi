from rest_framework import serializers
from .models import Movie, Genre


class MovieSerializer(serializers.ModelSerializer):
    genres = serializers.SerializerMethodField()

    def get_genres(self, instance):
        genre_list = instance.genre.all().values_list('name', flat=True)
        return genre_list

    class Meta:
        model = Movie
        fields = ('name', 'popularity', 'director', 'score', 'genres')
