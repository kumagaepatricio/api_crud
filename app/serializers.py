"""Serializer classes"""
from rest_framework import serializers

from .models import CustomUser


class CustomUserBaseSerializer(serializers.Serializer):
    """Class that serializes basic User data"""
    id = serializers.SerializerMethodField()
    username = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()

    @staticmethod
    def get_id(obj):
        return obj.uuid

    class Meta:
        """Definition of model and serialized fields"""
        model = CustomUser
        fields = ['id', 'username', 'first_name', 'last_name']


class CustomUserFullSerializer(CustomUserBaseSerializer):
    """Class that serializes full User data"""
    email = serializers.CharField()
    groups = serializers.SerializerMethodField()
    subscription = serializers.CharField()
    created = serializers.SerializerMethodField()
    updated = serializers.SerializerMethodField()

    @staticmethod
    def get_groups(obj):
        groups = []

        for group in obj.groups.all():
            groups.append(group.name)

        return groups

    @staticmethod
    def get_created(obj):
        return obj.date_joined

    @staticmethod
    def get_updated(obj):
        return obj.date_updated

    class Meta:
        """Definition of serialized fields"""
        fields = '__all__'
