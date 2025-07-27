from rest_framework import serializers
from .models import Event
from django.contrib.auth import get_user_model

User = get_user_model()


class UserMiniSerializer(serializers.ModelSerializer):
    """Minimal user serializer for organizer details."""
    class Meta:
        model = User
        fields = ("id", "username", "email")


class EventSerializer(serializers.ModelSerializer):
    organizer = UserMiniSerializer(read_only=True)
    date = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")


    class Meta:
        model = Event
        fields = [
            'id',
            'organizer',
            'title',
            'description',
            'location',
            'date',
            'max_attendees'
        ]
