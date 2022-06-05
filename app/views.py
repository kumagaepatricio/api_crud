from django.db import IntegrityError

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .models import CustomUser
from .serializers import CustomUserBaseSerializer, CustomUserFullSerializer
from .managers import UserManager
from .exceptions import PasswordException, ActionForbiddenException


class UserView(APIView):
    """Need to be logged in to perform any HTTP request"""
    permission_classes = (IsAuthenticated,)

    def get(self, request, uuid):
        user = CustomUser.objects.get(uuid=uuid)

        if request.user.is_staff or user.username == request.user.username:
            serializer = CustomUserFullSerializer(user)
        else:
            serializer = CustomUserBaseSerializer(user)

        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def post(self, request):

        try:

            user = UserManager.create_user(request)
            serializer = CustomUserFullSerializer(user)

            return Response(data=serializer.data, status=status.HTTP_201_CREATED)

        except (PasswordException, ActionForbiddenException) as message:
            return Response(data={'message': str(message)}, status=status.HTTP_400_BAD_REQUEST)
        except IntegrityError:
            return Response(data={'message': 'Already existing username'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, uuid):

        try:
            custom_user = CustomUser.objects.update_user(request, uuid)
            serializer = CustomUserFullSerializer(custom_user)

            return Response(data=serializer.data, status=status.HTTP_200_OK)
        except ActionForbiddenException as message:
            return Response(data={'message': str(message)}, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, uuid):

        try:
            UserManager.delete_user(request, uuid)

            return Response(status=status.HTTP_204_NO_CONTENT)
        except ActionForbiddenException as message:
            return Response(data={'message': str(message)}, status=status.HTTP_400_BAD_REQUEST)


