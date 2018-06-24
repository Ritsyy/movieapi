from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.settings import api_settings

import json

from .models import *
from .serializers import MovieSerializer, GenreSerializer


class MovieAPIView(APIView):
    allowed_methods = ['GET']
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
