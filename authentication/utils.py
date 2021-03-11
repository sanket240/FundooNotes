from django.core.mail import EmailMessage
from celery import shared_task
from notes.models import Notes
from django.contrib.auth.models import User
from datetime import datetime, timedelta


class Util:
    @shared_task
    def send_email(data):
        email = EmailMessage(
            subject=data['email_subject'], body=data['email_body'], to=[data['to_email']])
        email.send()

    @shared_task
    def send_reminder_email(email):
        try:
            notes = Notes.objects.filter(reminder__isnull=False)
            if notes:
                reminder_list = notes.values('id')
                for i in range(len(reminder_list)):
                    note_id = reminder_list[i]['id']
                    note = Notes.objects.get(id=note_id)
                    user = User.objects.get(id=note.owner_id)
                    print(user.username)
                    print(note.reminder)
                    reminder = note.reminder
                    if reminder.replace(tzinfo=None) - datetime.now() < timedelta(seconds=0):
                        print("Reminder Expired")
                    else:
                        if reminder.replace(tzinfo=None) - datetime.now() > timedelta(
                                hours=1):  # and reminder.replace(tzinfo=None)-datetime.now() < timedelta(hours=2):
                            email_body = 'Hi ' + user.username + \
                                         ' you have a reminder at ' + str(note.reminder)
                            data = {'email_body': email_body, 'to_email': user.email,
                                    'email_subject': 'Reminder'}
                            Util.send_email(data)

                            print('Sent Message')
        except Exception as e:
            print(e)
