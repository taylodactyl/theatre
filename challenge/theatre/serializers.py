from rest_framework import serializers
from .models import Room, Movie, Screening, Ticket


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ['id', 'capacity']


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ['id', 'title', 'length']


class ScreeningSerializer(serializers.ModelSerializer):
    class Meta:
        model = Screening
        fields = ['id', 'room', 'movie', 'time']


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ['id', 'screening']

