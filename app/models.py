"""Model classes"""
from django.db import models
from django.contrib.auth.models import User

from .managers import UserManager


class CustomUser(User):
    """Custom user class that extends from User"""
    uuid = models.CharField(max_length=255)
    subscription = models.CharField(max_length=100)
    date_updated = models.DateTimeField()

    objects = UserManager()

    class Meta:
        """Defining the name of the table"""
        db_table = 'custom_user'
