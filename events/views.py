from rest_framework import viewsets, filters, permissions, exceptions
from django_filters.rest_framework import DjangoFilterBackend
from .models import Event
from .serializers import EventSerializer
from .permissions import OrganizerPermission


class EventViewSet(viewsets.ModelViewSet):
    serializer_class = EventSerializer
    queryset = Event.objects.all().order_by('-date')
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['date', 'location']
    search_fields = ['title', 'description']

    def perform_create(self, serializer):
        """Set the current user as the event organizer."""
        serializer.save(organizer=self.request.user)

    def perform_update(self, serializer):
        """Only allow organizers who own the event to update it."""
        if serializer.instance.organizer != self.request.user:
            raise exceptions.PermissionDenied("You do not own this event")
        serializer.save()

    def perform_destroy(self, instance):
        """Only allow organizers who own the event to delete it."""
        if instance.organizer != self.request.user:
            raise exceptions.PermissionDenied("You do not own this event")
        instance.delete()

    def get_permissions(self):
        """Allow only authenticated organizers to modify events."""
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated(), OrganizerPermission()]
        return [permissions.IsAuthenticated()]
