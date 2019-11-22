from django.test import TestCase
from django.db.utils import IntegrityError
from .models import Room


class RoomModelTestCase(TestCase):
    def setUp(self):
        pass

    def test_no_negative_capacity(self):
        with self.assertRaises(IntegrityError):
            Room(capacity=-1).save()
