import datetime
from django.test import TestCase
from django.db.utils import IntegrityError
from django.urls import reverse
from .models import Room, Movie, Screening, Ticket
from rest_framework.test import APITestCase
from rest_framework import status


class RoomModelTestCase(TestCase):
    def setUp(self):
        pass

    def test_no_negative_capacity(self):
        with self.assertRaises(IntegrityError):
            Room(capacity=-1).save()


class ScreeningModelTestCase(TestCase):
    def setUp(self):
        self.room = Room(capacity=1)
        self.room.save()
        self.movie = Movie(title="blah")
        self.movie.save()
        self.today = datetime.date(year=2000, month=1, day=1)
        self.tomorrow = self.today + datetime.timedelta(days=1)
        self.yesterday = self.today - datetime.timedelta(days=1)
        self.current_time = datetime.datetime.combine(self.today, datetime.time(hour=1))

    def test_seats_remaining_when_there_are(self):
        screening = Screening(room=self.room, movie=self.movie, time=datetime.time(hour=10))
        self.assertTrue(screening.are_seats_remaining(self.today, current_time=self.current_time))

    def test_seats_remaining_when_sold_out(self):
        screening = Screening(room=self.room, movie=self.movie, time=datetime.time(hour=10))
        screening.save()
        ticket = Ticket(screening=screening, date=self.today)
        ticket.save()
        self.assertFalse(screening.are_seats_remaining(self.today, current_time=self.current_time))

    def test_seats_for_different_date_still_available(self):
        screening = Screening(room=self.room, movie=self.movie, time=datetime.time(hour=10))
        screening.save()
        ticket = Ticket(screening=screening, date=datetime.date(year=2000, month=1, day=1))
        ticket.save()
        self.assertTrue(screening.are_seats_remaining(self.tomorrow, current_time=self.current_time))

    def test_can_buy_tickets_for_tomorrow(self):
        screening = Screening(room=self.room, movie=self.movie, time=datetime.time(hour=10))
        screening.save()
        ticket = Ticket(screening=screening, date=self.tomorrow)
        ticket.save()
        self.assertFalse(screening.are_seats_remaining(self.tomorrow, current_time=self.current_time))

    def test_cannot_buy_tickets_for_yesterday(self):
        screening = Screening(room=self.room, movie=self.movie, time=datetime.time(hour=10))
        screening.save()
        ticket = Ticket(screening=screening, date=self.tomorrow)
        ticket.save()
        self.assertFalse(screening.are_seats_remaining(self.tomorrow, current_time=self.current_time))


class RoomApiTestCase(APITestCase):

    def test_successful_get_status(self):
        response = self.client.get('http://testserver/rooms/')
        self.assertEquals(response.status_code, 200)

    def test_post_single_room(self):
        url = reverse('room-list')
        data = {'capacity': '25'}
        self.client.post(url, data, format='json')
        self.assertEqual(Room.objects.count(), 1)

    def test_room_capacity_saved(self):
        capacity = 25
        url = reverse('room-list')
        data = {'capacity': '{}'.format(capacity)}
        self.client.post(url, data, format='json')
        self.assertEqual(Room.objects.get().capacity, capacity)

    def test_room_delete(self):
        list_url = reverse('room-list')
        detail_url = reverse('room-detail', args=['1'])
        data = {'capacity': '25'}
        self.client.post(list_url, data, format='json')
        self.client.delete(detail_url, format='json')
        self.assertEqual(Room.objects.count(), 0)

    def test_no_negative_capacity_saved(self):
        capacity = -10
        url = reverse('room-list')
        data = {'capacity': '{}'.format(capacity)}
        # TODO: Return proper error status instead of allowing
        #       database errors to escape
        with self.assertRaises(IntegrityError):
            self.client.post(url, data, format='json')


class MovieApiTestCase(APITestCase):

    def test_successful_get_status(self):
        response = self.client.get('http://testserver/movies/')
        self.assertEquals(response.status_code, 200)

    def test_post_single_movie(self):
        url = reverse('movie-list')
        data = {'title': 'blah'}
        self.client.post(url, data, format='json')
        self.assertEqual(Movie.objects.count(), 1)

    def test_movie_title_saved(self):
        title = 'blah'
        url = reverse('movie-list')
        data = {'title': '{}'.format(title)}
        self.client.post(url, data, format='json')
        self.assertEqual(Movie.objects.get().title, title)

    def test_movie_length_saved(self):
        length = datetime.timedelta(hours=2, minutes=2, seconds=2)
        url = reverse('movie-list')
        data = {'length': '{}'.format(length), 'title': 'blah'}
        self.client.post(url, data, format='json')
        self.assertEqual(Movie.objects.get().length, length)

    def test_movie_delete(self):
        list_url = reverse('movie-list')
        detail_url = reverse('movie-detail', args=['1'])
        data = {'title': 'blah'}
        self.client.post(list_url, data, format='json')
        self.client.delete(detail_url, format='json')
        self.assertEqual(Movie.objects.count(), 0)


class ScreeningApiTestCase(APITestCase):
    def setUp(self):
        self.room = Room(capacity=20)
        self.room.save()
        Movie(title="blah").save()
        self.time = datetime.time(hour=5)
        self.data = {'movie': '1', 'room': '1',
                     'time': "{}".format(self.time)}
        # TODO: there is probably a better way to isolate these tests from time of day
        self.data_for_ticket = {'date': "{}".format(datetime.date.today() + datetime.timedelta(days=1))}

    def test_successful_get_status(self):
        response = self.client.get('/screenings/')
        self.assertEquals(response.status_code, 200)

    def test_post_single_screening(self):
        url = reverse('screening-list')
        data = {'movie': '1', 'room': '1',
                'time': "{}".format(datetime.time(hour=5))}
        self.client.post(url, data, format='json')
        self.assertEqual(Screening.objects.count(), 1)

    def test_screening_time_saved(self):
        url = reverse('screening-list')
        self.client.post(url, self.data, format='json')
        self.assertEqual(Screening.objects.filter(time=self.time).count(), 1)

    def test_screening_delete(self):
        list_url = reverse('screening-list')
        detail_url = reverse('screening-detail', args=['1'])
        self.client.post(list_url, self.data, format='json')
        self.client.delete(detail_url, format='json')
        self.assertEqual(Screening.objects.count(), 0)

    def add_screening(self, data=None):
        list_url = reverse('screening-list')
        if data is None:
            data = self.data
        return self.client.post(list_url, data, format='json')

    def test_cannot_add_overlapping_screening(self):
        data = {'movie': '1', 'room': '1',
                'time': "{}".format(datetime.time(hour=5, minute=30))}
        self.add_screening()  # Add screening at 5
        response = self.add_screening(data)
        self.assertTrue(status.is_client_error(response.status_code))

    def test_buy_ticket_success(self):
        self.add_screening()
        buy_ticket_url = reverse('screening-buyticket', args=['1'])
        response = self.client.post(buy_ticket_url, data=self.data_for_ticket, format='json')
        self.assertTrue(status.is_success(response.status_code))

    def test_buy_one_ticket(self):
        self.add_screening()
        buy_ticket_url = reverse('screening-buyticket', args=['1'])
        self.client.post(buy_ticket_url, data=self.data_for_ticket, format='json')
        self.assertEqual(Ticket.objects.count(), 1)

    def test_buy_ticket_for_correct_screening(self):
        screening_id = 1
        self.add_screening()
        buy_ticket_url = reverse('screening-buyticket', args=['{}'.format(screening_id)])
        response = self.client.post(buy_ticket_url, data=self.data_for_ticket, format='json')
        self.assertEqual(screening_id, response.data['screening'])

    def test_no_more_tickets_than_seats(self):
        self.add_screening()
        buy_ticket_url = reverse('screening-buyticket', args=['1'])
        for _ in range(self.room.capacity):  # Buy all the tickets
            self.client.post(buy_ticket_url, data=self.data_for_ticket, format='json')

        # Buy one more ticket and get rejected
        response = self.client.post(buy_ticket_url, data=self.data_for_ticket, format='json')
        self.assertTrue(status.is_client_error(response.status_code))

    def test_no_ticket_for_bogus_date(self):
        bad_data_for_ticket = {'date': "asdfasdf"}
        self.add_screening()
        buy_ticket_url = reverse('screening-buyticket', args=['1'])
        response = self.client.post(buy_ticket_url, data=bad_data_for_ticket, format='json')
        self.assertTrue(status.is_client_error(response.status_code))


class ScreeningOverlapTestCase(APITestCase):
    def setUp(self):
        self.room = Room(capacity=20)
        self.room.save()
        self.first_movie = Movie(title="first", length=datetime.timedelta(hours=1))
        self.second_movie = Movie(title="second", length=datetime.timedelta(hours=1))
        self.first_movie.save()
        self.second_movie.save()

    # movie 1: |===========|
    # movie 2:              |===========|
    def test_no_overlap_is_fine(self):
        screening_one = Screening(room=self.room, movie=self.first_movie, time=datetime.time(hour=5))
        screening_two = Screening(room=self.room, movie=self.second_movie, time=datetime.time(hour=6))
        self.assertFalse(screening_one.overlaps(screening_two))

    # movie 1: |===========|
    # movie 2:       |===========|
    # check if movie 1 knows it overlaps
    def test_left_overlap_fails(self):
        screening_one = Screening(room=self.room, movie=self.first_movie, time=datetime.time(hour=5, minute=30))
        screening_two = Screening(room=self.room, movie=self.second_movie, time=datetime.time(hour=6))
        self.assertTrue(screening_one.overlaps(screening_two))

    # movie 1: |===========|
    # movie 2:       |===========|
    # check if movie 2 knows it overlaps
    def test_right_overlap_fails(self):
        screening_one = Screening(room=self.room, movie=self.first_movie, time=datetime.time(hour=5, minute=30))
        screening_two = Screening(room=self.room, movie=self.second_movie, time=datetime.time(hour=6))
        self.assertTrue(screening_two.overlaps(screening_one))

    # movie 1: |========================|
    # movie 2:       |===========|
    # check if movie 1 knows it overlaps
    def test_containment_fails_when_containing(self):
        three_hour_movie = Movie(title="long", length=datetime.timedelta(hours=3))
        screening_one = Screening(room=self.room, movie=three_hour_movie, time=datetime.time(hour=5))
        screening_two = Screening(room=self.room, movie=self.second_movie, time=datetime.time(hour=6))
        self.assertTrue(screening_one.overlaps(screening_two))

    # movie 1: |========================|
    # movie 2:       |===========|
    # check if movie 2 knows it overlaps
    def test_containment_fails_when_contained(self):
        three_hour_movie = Movie(title="long", length=datetime.timedelta(hours=3))
        screening_one = Screening(room=self.room, movie=three_hour_movie, time=datetime.time(hour=5))
        screening_two = Screening(room=self.room, movie=self.second_movie, time=datetime.time(hour=6))
        self.assertTrue(screening_two.overlaps(screening_one))

