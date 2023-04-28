from django.test import Client, TestCase
from django.urls import reverse

# Create your tests here.

client = Client()

class InitScreeningTest(TestCase):

    def test_create(self):

        data = {
            'candidate':1
        }

        response = client.post(reverse('main:initscreening.create'), data=data)

        # Assert that the response status code is 200 OK
        self.assertEqual(response.status_code, 200)

    def test_proceed(self):

        data = {
            'proceed':1,
            'initial_screening':1,
        }

        response = client.post(reverse('main:initscreening.update'), data=data)

        # Assert that the response status code is 200 OK
        self.assertEqual(response.status_code, 200)


class PrescreeningTest(TestCase):

    def test_create(self):

        data = {
            'candidate':1
        }

        response = client.post(reverse('main:prescreening.create'), data=data)

        # Assert that the response status code is 200 OK
        self.assertEqual(response.status_code, 200)

    def test_proceed(self):

        data = {
            'proceed':1,
            'prescreening':1,
        }

        response = client.post(reverse('main:prescreening.update'), data=data)

        # Assert that the response status code is 200 OK
        self.assertEqual(response.status_code, 200)


class CBITest(TestCase):


    def test_create(self):

        data = {
            'candidate':1
        }

        response = client.post(reverse('main:cbi.create'), data=data)

        # Assert that the response status code is 200 OK
        self.assertEqual(response.status_code, 200)

    def test_schedule_create(self):

        data = {
            'cbi':1,
            'datetime':'2023-04-30 12:30:00',
            'assessor1':1,
            'assessor2':2,
        }

        response = client.post(reverse('main:cbi.update'), data=data)

        # Assert that the response status code is 200 OK
        self.assertEqual(response.status_code, 200)

