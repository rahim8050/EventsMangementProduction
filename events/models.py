from django.db import models
from django.conf import settings


class Event(models.Model):
    """Event created by an organizer."""
    organizer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='events')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    location = models.CharField(max_length=255)
    date = models.DateTimeField()
    max_attendees = models.PositiveIntegerField()

    def __str__(self):
        return self.title
