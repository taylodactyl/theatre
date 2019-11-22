from django.test import TestCase
from django.db.utils import IntegrityError
from django.urls import reverse
from .models import Room
from rest_framework.test import RequestsClient
from rest_framework.test import APITestCase

class RoomModelTestCase(TestCase):
    def setUp(self):
        pass

    def test_no_negative_capacity(self):
        with self.assertRaises(IntegrityError):
            Room(capacity=-1).save()


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

    def test_no_negative_capacity_saved(self):
        capacity = -10
        url = reverse('room-list')
        data = {'capacity': '{}'.format(capacity)}
        # TODO: Return proper error status instead of allowing
        #       database errors to escape
        with self.assertRaises(IntegrityError):
            self.client.post(url, data, format='json')
