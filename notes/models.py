from django.db import models
from django.contrib.auth.models import User


class Labels(models.Model):
    name = models.TextField(db_index=True)
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True, null=False, blank=False)

    def get_name(self):
        return self.name


class Notes(models.Model):
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE)
    title = models.CharField(max_length=30)
    description = models.CharField(max_length=150)
    date = models.DateTimeField(auto_now_add=True, null=False, blank=False)
    collaborator = models.ManyToManyField(to=User, related_name='collaborator')
    label = models.ManyToManyField(to=Labels)

    def get_description(self):
        return self.description

    def get_owner(self):
        return self.owner
