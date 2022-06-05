from django.db import models
from django.contrib.auth.models import User

from .managers import UserManager

class CustomUser(User):

    uuid = models.CharField(max_length=255)
    subscription = models.CharField(max_length=100)
    date_updated = models.DateTimeField()

    objects = UserManager()

    class Meta:
        db_table = 'custom_user'
