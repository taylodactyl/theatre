from django.db import models
from datetime import timedelta


class Room(models.Model):
    capacity = models.IntegerField(default=100)


class Movie(models.Model):
    title = models.CharField(max_length=200)
    length = models.DurationField(default=timedelta(minutes=90))


class Screening(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    time = models.TimeField()


class Ticket(models.Model):
    showing = models.ForeignKey(Screening, on_delete=models.CASCADE)

