from django.core.mail import EmailMessage
from celery import shared_task
from notes.models import Notes
from django.contrib.auth.models import User


class Util:
    @shared_task
    def send_email(data):
        email = EmailMessage(
            subject=data['email_subject'], body=data['email_body'], to=[data['to_email']])
        email.send()

    @shared_task
    def send_reminder_email(email):
        print('Send Reminder Email')
        print(f'Celery Beat{email}')
        note = Notes.objects.get(owner_id=1)
        user = User.objects.get(id=1)
        mail = EmailMessage(
            subject='Reminder', body='Hi ' + user.username + 'U have a reminder at' + note.reminder, to=user.email)
        mail.send()



