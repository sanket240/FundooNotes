from django.test import TestCase
from ..models import Notes
from django.contrib.auth.models import User


class NotesTest(TestCase):

    def setUp(self):
        self.user = User.objects.create(email='sivanarayn@gmail.com', username='siva',
                                        password='Siva@123')
        Notes.objects.create(title='Exam', description='Tommorow is Exam', owner=self.user)

    def test_create_note(self):
        note = Notes.objects.get(title='Exam')
        self.assertEqual(note.get_description(), "Tommorow is Exam")
