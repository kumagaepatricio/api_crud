"""Views from the main app"""
import logging

from django.db import IntegrityError

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .models import CustomUser
from .serializers import CustomUserBaseSerializer, CustomUserFullSerializer
from .managers import UserManager
from .exceptions import PasswordException, ActionForbiddenException

logger = logging.getLogger('api_crud')

class UserView(APIView):
    """Need to be logged in to perform any HTTP request"""
    permission_classes = (IsAuthenticated,)

    @staticmethod
    def get(request, uuid):
        """GET method that obtains a user from the DB.
        If user is admin or getting self info gets full data,
        otherwise will get basic data"""
        user = CustomUser.objects.get(uuid=uuid)

        if request.user.is_staff or user.username == request.user.username:
            serializer = CustomUserFullSerializer(user)
        else:
            serializer = CustomUserBaseSerializer(user)

        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @staticmethod
    def post(request):
        """POST method to create a new user"""
        try:

            user = UserManager.create_user(request)
            serializer = CustomUserFullSerializer(user)

            return Response(data=serializer.data, status=status.HTTP_201_CREATED)

        except (PasswordException, ActionForbiddenException) as message:
            return Response(data={'message': str(message)}, status=status.HTTP_400_BAD_REQUEST)
        except IntegrityError as integrity_error:
            return Response(data={'message': str(integrity_error)},
                            status=status.HTTP_400_BAD_REQUEST)
        except Exception as exc:
            logger.error(str(exc))
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    @staticmethod
    def put(request, uuid):
        """PUT method to update an existing user"""
        try:
            custom_user = CustomUser.objects.update_user(request, uuid)
            serializer = CustomUserFullSerializer(custom_user)

            return Response(data=serializer.data, status=status.HTTP_200_OK)
        except ActionForbiddenException as message:
            return Response(data={'message': str(message)}, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def delete(request, uuid):
        """DELETE method to delete a user"""
        try:
            UserManager.delete_user(request, uuid)

            return Response(status=status.HTTP_204_NO_CONTENT)
        except ActionForbiddenException as message:
            return Response(data={'message': str(message)}, status=status.HTTP_400_BAD_REQUEST)
