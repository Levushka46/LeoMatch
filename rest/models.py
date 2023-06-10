from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    avatar = models.ImageField(upload_to='avatars/')  # аватар
    sex = models.CharField(max_length=100, null=False)  # пол
    match = models.ManyToManyField('self', blank=True)  # совпадение симпатии
    outgoing_match_requests = models.ManyToManyField(
        'self', symmetrical=False, related_name='incoming_match_requests', blank=True)  # исходящие симпатии

    def __str__(self):
        return self.email
