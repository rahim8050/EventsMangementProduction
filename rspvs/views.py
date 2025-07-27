from rest_framework import viewsets, permissions, status, serializers
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import RSVP
from .serializers import RSVPSerializer
from events.models import Event
from .permissions import OrganizerPermission


class RSVPViewSet(viewsets.ModelViewSet):
    serializer_class = RSVPSerializer
    queryset = RSVP.objects.all()

    def perform_create(self, serializer):
        """Ensure the event has not reached max attendees."""
        event = serializer.validated_data['event']
        if event.rsvps.filter(approved=True).count() >= event.max_attendees:
            raise serializers.ValidationError('Event capacity reached')
        serializer.save(user=self.request.user)

    def get_permissions(self):
        """Dynamic permission handling based on action."""
        if self.action == 'approve':
            return [permissions.IsAuthenticated(), OrganizerPermission()]
        return [permissions.IsAuthenticated()]

    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        """Approve an RSVP if the user is the event organizer."""
        rsvp = self.get_object()

        if rsvp.event.organizer != request.user:
            return Response({'detail': 'Not allowed'}, status=status.HTTP_403_FORBIDDEN)

        if rsvp.event.rsvps.filter(approved=True).count() >= rsvp.event.max_attendees:
            return Response({'detail': 'Event capacity reached'}, status=status.HTTP_400_BAD_REQUEST)

        rsvp.approved = True
        rsvp.save()
        return Response(self.get_serializer(rsvp).data)
