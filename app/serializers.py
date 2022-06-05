from rest_framework import serializers

from .models import CustomUser


class CustomUserBaseSerializer(serializers.Serializer):
    id = serializers.SerializerMethodField()
    username = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()

    def get_id(self, obj):
        return obj.uuid

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'first_name', 'last_name']


class CustomUserFullSerializer(CustomUserBaseSerializer):

    email = serializers.CharField()
    groups = serializers.SerializerMethodField()
    subscription = serializers.CharField()
    created = serializers.SerializerMethodField()
    updated = serializers.SerializerMethodField()

    def get_groups(self, obj):
        groups = []

        for group in obj.groups.all():
            groups.append(group.name)

        return groups

    def get_created(self, obj):
        return obj.date_joined

    def get_updated(self, obj):
        return obj.date_updated

    class Meta:
        fields = '__all__'