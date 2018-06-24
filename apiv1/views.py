from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.settings import api_settings

import json

from .models import *
from .serializers import MovieSerializer


class MovieAPIView(APIView):
    allowed_methods = ['GET', 'POST', 'PUT']
    serializer_class = MovieSerializer
    pagination_class = api_settings.DEFAULT_PAGINATION_CLASS

    def get(self, request):
        queryset = Movie.objects.all()

        name = request.query_params.get('name', None)
        if name is not None:
            queryset = queryset.filter(name__icontains=name)

        director = request.query_params.get('director', None)
        if director is not None:
            queryset = queryset.filter(director__icontains=director)

        # filter if movie has genre with queried genre name
        genre = request.query_params.get('genre', None)
        if genre is not None:
            queryset = queryset.filter(genre__name__icontains=genre)

        paginator = self.pagination_class()
        result_page = paginator.paginate_queryset(queryset, request)

        serializer = MovieSerializer(result_page, many=True, context={
            'request': request
        })
        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        serializer = MovieSerializer(data=request.data)
        genres = request.data.get('genres')
        if serializer.is_valid():
            movie = serializer.save()
            for item in genres:
                genre_name = item.strip()
                genre, created = Genre.objects.get_or_create(name=genre_name)
                movie.genre.add(genre)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        movie_id = request.data.get('id')
        movie = Movie.objects.filter(id=movie_id).first()
        if not movie:
            # If movie does not exist, create it
            self.post(request)
        # Update the movie
        movie.name = request.data.get('name')
        movie.popularity = request.data.get('popularity')
        movie.score = request.data.get('score')
        movie.director = request.data.get('director')
        movie.save()
        genres = request.data.get('genres')
        movie.genre.all().delete()  # clear existing genres for this movie
        for item in genres:
            genre_name = item.strip()
            genre, created = Genre.objects.get_or_create(name=genre_name)
            movie.genre.add(genre)
        return Response({'message': "updated movie"}, status=status.HTTP_200_OK)

    def delete(self, request):
        movie_id = request.data.get('id')
        movie = Movie.objects.filter(id=movie_id).first()
        if not movie:
            return Response({'message': "not found"}, status=status.HTTP_400_BAD_REQUEST)
        movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

