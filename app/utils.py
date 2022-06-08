"""Utils class for validations"""
import re

from django.contrib.auth.hashers import check_password

from .exceptions import PasswordException, ActionForbiddenException


class Utils:

    @staticmethod
    def check_passwords(password, repeat_password):
        """This method checks that both passwords match and
        minimum requirements"""

        if password != repeat_password:
            raise PasswordException('Passwords don\'t match')

        if not re.search('^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$', password):
            raise PasswordException('Password must contain at least one lowercase letter, one uppercase letter, one digit and at least a length of 8')

    @staticmethod
    def can_delete(logged_user, delete_user):
        """This method checks if logged user can delete a user"""
        if not logged_user.is_superuser:
            if not logged_user.is_staff or (logged_user.is_staff and delete_user.is_staff):
                raise ActionForbiddenException('Can not perform this action')

    @staticmethod
    def can_create(user):
        """This method checks if logged user can create a user"""
        if not user.is_staff and not user.is_superuser:
            raise ActionForbiddenException('Can not perform this action')

    @staticmethod
    def can_update(logged_user, update_user):
        """This method checks if logged user can update a user"""
        if not logged_user.is_staff and not logged_user.username == update_user.username:
            raise ActionForbiddenException('Can not perform this action')


    @staticmethod
    def can_update_password(request, user):
        """This method checks if logged user can modify
        everyone or personal password"""
        can_update = True
        if not user.is_staff:
            if not check_password(request.data.get('old_password'), user.password):
                can_update = False
        return can_update

    @staticmethod
    def can_update_email(email):
        """This method checks if a user can update an e-mail"""
        from .models import CustomUser
        can_update = True
        email = CustomUser.objects.filter(email=email)
        if email:
            can_update = False
        return can_update

    @staticmethod
    def can_update_groups(logged_user):
        """This method checks if a user can update groups"""
        can_update = True
        if not logged_user.is_staff:
            can_update = False

        return can_update
