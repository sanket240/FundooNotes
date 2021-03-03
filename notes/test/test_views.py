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
        self.token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6ImFkbWluMyJ9.8MpjthUPGQrHh7GUtn2eOSaobGjNVdjwumR6IvG3r9o"
        self.api_authentication()

        self.create_note_for_valid_token = {
            'title': 'Good Morning',
            'description': 'Happy Friday',
        }

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token)

    def test_get_notes(self):
        respone=self.client.get(reverse('create'))
        self.assertEqual(respone.status_code,status.HTTP_200_OK)

    def test_create_notes_with_valid_payload(self):
        response = self.client.post(reverse('create'), data=json.dumps(self.create_note_for_valid_token),
                                    content_type=CONTENT_TYPE)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

