from rest_framework import status
from django.test import TestCase, Client
from django.urls import reverse
from ..models import Notes
from ..serializers import NotesSerializer
from django.contrib.auth.models import User
import json
from rest_framework.test import APITestCase

CONTENT_TYPE = 'application/json'


class NotesAPITest(APITestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create(email='amit@gmail.com', username='amit',
                                        password='Amit@123')
        self.user_login_payload = {
            "username": "admin1",
            "email": "admin1@gmail.com",
            "password": "Sanket@123"
        }

        self.user_login_invalid_payload = {
            'username': 'admin1222',
            'password': 'Sanket@123'
        }
        self.add_notes_payload = {

            "title": "Wake Up Man Hello",
            "description": "Tommorow is Birthday"

        }

        self.update_notes = {
            "title": "Wake Up Man Hello",
            "description":
                "Tommorow is Exam"

        }

    def login_method(self, credentials):
        login = self.client.post(reverse('login'), data=json.dumps(credentials), content_type=CONTENT_TYPE)
        token = login.get('authorization')
        auth_headers = {
            'HTTP_AUTHORIZATION': token,
        }
        return auth_headers

    def test_create_notes_valid_payload(self):
        auth_headers = self.login_method(self.user_login_payload)
        response = self.client.post(reverse('create'), **auth_headers, data=json.dumps(self.add_notes_payload),
                                    content_type=CONTENT_TYPE)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_notes_invalid_payload(self):
        auth_headers = self.login_method(self.user_login_invalid_payload)
        response = self.client.post(reverse('create'), **auth_headers, data=json.dumps(self.add_notes_payload),
                                    content_type=CONTENT_TYPE)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_all_notes_valid_user(self):
        auth_headers = self.login_method(self.user_login_payload)
        response = self.client.get(reverse('create'), **auth_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_all_notes_invalid_user(self):
        auth_headers = self.login_method(self.user_login_invalid_payload)
        response = self.client.get(reverse('create'), **auth_headers)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_notes_with_valid_user(self):
        auth_headers = self.login_method(self.user_login_payload)
        response = self.client.put(reverse('notes', **auth_headers, kwargs={'id': 12}),
                                   data=json.dumps(self.update_notes), content_type=CONTENT_TYPE)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_notes_with_invalid_user(self):
        auth_headers = self.login_method(self.user_login_invalid_payload)
        response = self.client.put(reverse('notes', **auth_headers, kwargs={'id': 12}),
                                   data=json.dumps(self.update_notes), content_type=CONTENT_TYPE)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_notes_valid_user(self):
        auth_headers = self.login_method(self.user_login_payload)
        response = self.client.get(reverse('notes'), **auth_headers, kwargs={'id': 12})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_notes_invalid_user(self):
        auth_headers = self.login_method(self.user_login_invalid_payload)
        response = self.client.delete(reverse('notes'), **auth_headers, kwargs={'id': 12})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
