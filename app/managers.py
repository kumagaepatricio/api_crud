"""Managers file with DB interaction methods"""
import uuid
import datetime
import responses
import requests

from django.db   import models
from django.contrib.auth.models import Group

from .utils import Utils


class UserManager(models.Manager):
    """This class includes all User related methods"""

    @staticmethod
    def create_user(request):
        """Method called from view to create a user.
        Includes user creation and validations"""
        from .models import CustomUser

        Utils.can_create(request.user)
        Utils.check_passwords(request.data.get('password'), request.data.get('repeat_password'))

        new_uuid = uuid.uuid4()

        user = CustomUser.objects.create(
            username=request.data.get('username'),
            first_name=request.data.get('first_name'),
            last_name=request.data.get('last_name'),
            email=request.data.get('email'),
            uuid=new_uuid,
            date_updated=datetime.datetime.now(),
            subscription=UserManager.get_subscription(new_uuid)
        )

        user.set_password(request.data.get('password'))

        user = UserManager.set_user_groups(user, request.data.get('groups'))

        user.save()

        return user

    @staticmethod
    def update_user(request, user_uuid):
        """Method that updates a user"""
        from .models import CustomUser

        custom_user = CustomUser.objects.get(uuid=user_uuid)

        Utils.can_update(request.user, custom_user)

        custom_user.first_name = request.data.get('first_name')
        custom_user.last_name = request.data.get('last_name')
        if Utils.can_update_email(request.data.get('email')):
            custom_user.email = request.data.get('email')
        if Utils.can_update_password(request, custom_user):
            custom_user.set_password(request.data.get('password'))

        custom_user.date_updated = datetime.datetime.now()
        custom_user.save()

        return custom_user


    @staticmethod
    def delete_user(request, user_uuid):
        """Method that deletes a user"""
        from .models import CustomUser
        delete_user = CustomUser.objects.get(uuid=user_uuid)
        Utils.can_delete(request.user, delete_user)
        CustomUser.objects.get(uuid=user_uuid).delete()

    @staticmethod
    def set_user_groups(user, groups):
        """Method user to set groups to users on creation"""
        for group in groups:

            try:
                user.groups.add(Group.objects.get(name=group))
            except Group.DoesNotExist:
                """Non existing group created on demand"""
                user.groups.add(GroupManager.create_group(group))

        return user

    @staticmethod
    @responses.activate
    def get_subscription(new_uuid):
        """Mocked method"""
        subscription_response = responses.Response(
            method="GET",
            url="https://subscriptions.fake.service.test/api/v1/users/:uuid",
            json={"id": str(new_uuid), "subscription": "active"},
            status=200
        )

        responses.add(subscription_response)

        req = requests.get('https://subscriptions.fake.service.test/api/v1/users/:uuid',
                           data={'uuid': new_uuid})

        return req.json()['subscription']


class GroupManager(models.Manager):
    """Manager with Group related methods"""

    @staticmethod
    def create_group(name):
        """Method that creates a Group"""
        return Group.objects.create(name=name)
