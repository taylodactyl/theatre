from theatre.models import Room, Movie, Screening, Ticket
from theatre.serializers import RoomSerializer, MovieSerializer, ScreeningSerializer, TicketSerializer
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
import datetime


class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer


class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer


class ScreeningViewSet(viewsets.ModelViewSet):
    queryset = Screening.objects.all()
    serializer_class = ScreeningSerializer

    @action(detail=True, url_path='buyticket', url_name='buyticket')
    def buy_ticket(self, request, *args, **kwargs):
        ticket = Ticket(screening=self.get_object(), date=datetime.date.today())
        ticket.save()
        return Response(TicketSerializer(ticket).data)
