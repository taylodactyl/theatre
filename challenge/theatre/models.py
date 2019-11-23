from django.db import models
import datetime


class Room(models.Model):
    capacity = models.PositiveIntegerField(default=100)

    def __str__(self):
        return "{} - Seats {}".format(self.id, self.capacity)


class Movie(models.Model):
    title = models.CharField(max_length=200)
    length = models.DurationField(default=datetime.timedelta(minutes=90))

    def __str__(self):
        return "{} - {}".format(self.title, self.length)


class Screening(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    time = models.TimeField()

    def are_seats_remaining(self):
        return self.ticket_set.count() < self.room.capacity

    def overlaps(self, other_screening):
        # Overlap calc inspired by https://stackoverflow.com/a/9044111
        start1 = datetime.datetime.combine(datetime.date.today(), self.time)
        start2 = datetime.datetime.combine(datetime.date.today(), other_screening.time)
        end1 = start1 + self.movie.length
        end2 = start2 + other_screening.movie.length
        latest_start = max(start1, start2)
        earliest_end = min(end1, end2)
        overlap = (earliest_end - latest_start)
        return overlap > datetime.timedelta(0)

    def __str__(self):
        return "{} - {} @ {}".format(self.room, self.movie, self.time)


class Ticket(models.Model):
    screening = models.ForeignKey(Screening, on_delete=models.CASCADE)
    date = models.DateField()

    def __str__(self):
        return "{} - {}".format(self.screening, self.date)

