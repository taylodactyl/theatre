from theatre.models import Room, Movie
from theatre.serializers import RoomSerializer, MovieSerializer
from rest_framework import viewsets


class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer


class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
