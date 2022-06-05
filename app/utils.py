import re

from django.contrib.auth.hashers import check_password

from .exceptions import PasswordException, ActionForbiddenException

class Utils:

    @staticmethod
    def check_passwords(password, repeat_password):

        if password != repeat_password:
            raise PasswordException('Passwords don\'t match')

        if not re.search('^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$', password):
            raise PasswordException('Password must contain at least one lowercase letter, one uppercase letter, one digit and at least a length of 8')

    @staticmethod
    def can_delete(logged_user, delete_user):
        if not logged_user.is_superuser:
            if not logged_user.is_staff or (logged_user.is_staff and delete_user.is_staff):
                raise ActionForbiddenException('Can not perform this action')

    @staticmethod
    def can_create(user):
        if not user.is_staff and not user.is_superuser:
            raise ActionForbiddenException('Can not perform this action')

    @staticmethod
    def can_update(logged_user, update_user):
        if not logged_user.is_staff:
            raise ActionForbiddenException('Can not perform this action')


    @staticmethod
    def can_update_password(request, user):
        if not user.is_staff:
            if not check_password(request.data.get('password'), user.password):
                raise ActionForbiddenException('Can not change user password')

    @staticmethod
    def can_update_groups(logged_user):
        if not logged_user.is_staff:
            raise ActionForbiddenException('Can not update groups')