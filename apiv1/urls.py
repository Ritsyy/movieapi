from django.conf.urls import include, url
from . import views


urlpatterns = [
    url(r'^movies/$', views.MovieAPIView.as_view(), name='api-movies-list'),
]
