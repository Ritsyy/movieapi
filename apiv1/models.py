from __future__ import unicode_literals

from django.db import models


class Genre(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Movie(models.Model):
    popularity = models.FloatField()
    director = models.CharField(max_length=100)
    genre = models.ManyToManyField(Genre)
    score = models.FloatField()
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name
