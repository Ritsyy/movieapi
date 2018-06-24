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
        movies = Movie.objects.all()
        paginator = self.pagination_class()
        result_page = paginator.paginate_queryset(movies, request)
        serializer = MovieSerializer(result_page, many=True, context={
            'request': request
        })
        return paginator.get_paginated_response(serializer.data)
