from django.db import models
from datetime import timedelta, date


class Room(models.Model):
    capacity = models.PositiveIntegerField(default=100)

    def __str__(self):
        return "{} - Seats {}".format(self.id, self.capacity)


class Movie(models.Model):
    title = models.CharField(max_length=200)
    length = models.DurationField(default=timedelta(minutes=90))

    def __str__(self):
        return "{} - {}".format(self.title, self.length)


class Screening(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    time = models.TimeField()

    def are_seats_remaining(self):
        return self.ticket_set.count() < self.room.capacity

    def __str__(self):
        return "{} - {} @ {}".format(self.room, self.movie, self.time)


class Ticket(models.Model):
    screening = models.ForeignKey(Screening, on_delete=models.CASCADE)
    date = models.DateField()

    def __str__(self):
        return "{} - {}".format(self.screening, self.date)

