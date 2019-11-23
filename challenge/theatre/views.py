from theatre.models import Room, Movie, Screening, Ticket
from theatre.serializers import RoomSerializer, MovieSerializer, ScreeningSerializer, TicketSerializer
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.http import HttpResponseBadRequest
import datetime


class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer


class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer


def overlap_exists(proposed_screening):
    for screening in Screening.objects.all():
        if proposed_screening.overlaps(screening):
            return True
    return False


class ScreeningViewSet(viewsets.ModelViewSet):
    queryset = Screening.objects.all()
    serializer_class = ScreeningSerializer

    @action(detail=True, url_path='buyticket', url_name='buyticket')
    def buy_ticket(self, request, *args, **kwargs):
        if self.get_object().are_seats_remaining():
            ticket = Ticket(screening=self.get_object(), date=datetime.date.today())
            ticket.save()
            return Response(TicketSerializer(ticket).data)
        else:
            return HttpResponseBadRequest("Screening sold out")

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        proposed_screening = Screening(**serializer.validated_data)
        if overlap_exists(proposed_screening):
            return HttpResponseBadRequest("Overlaps existing screening")
        return super(ScreeningViewSet, self).create(request, args, kwargs)

