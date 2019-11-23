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

    def test_seats_remaining_when_there_are(self):
        screening = Screening(room=self.room, movie=self.movie, time=datetime.time(hour=10))
        self.assertTrue(screening.are_seats_remaining())

    def test_seats_remaining_when_sold_out(self):
        screening = Screening(room=self.room, movie=self.movie, time=datetime.time(hour=10))
        screening.save()
        ticket = Ticket(screening=screening, date=datetime.date.today())
        ticket.save()
        self.assertFalse(screening.are_seats_remaining())


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

    def add_screening(self):
        list_url = reverse('screening-list')
        self.client.post(list_url, self.data, format='json')

    def test_buy_ticket_success(self):
        self.add_screening()
        buy_ticket_url = reverse('screening-buyticket', args=['1'])
        response = self.client.get(buy_ticket_url)
        self.assertTrue(status.is_success(response.status_code))

    def test_buy_one_ticket(self):
        self.add_screening()
        buy_ticket_url = reverse('screening-buyticket', args=['1'])
        self.client.get(buy_ticket_url)
        self.assertEqual(Ticket.objects.count(), 1)

    def test_buy_ticket_for_correct_screening(self):
        screening_id = 1
        self.add_screening()
        buy_ticket_url = reverse('screening-buyticket', args=['{}'.format(screening_id)])
        response = self.client.get(buy_ticket_url)
        self.assertEqual(screening_id, response.data['screening'])

    def test_no_more_tickets_than_seats(self):
        self.add_screening()
        buy_ticket_url = reverse('screening-buyticket', args=['1'])
        for _ in range(self.room.capacity):  # Buy all the tickets
            self.client.get(buy_ticket_url)

        # Buy one more ticket and get rejected
        response = self.client.get(buy_ticket_url)
        self.assertTrue(status.is_client_error(response.status_code))
