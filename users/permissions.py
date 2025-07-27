from rest_framework.permissions import BasePermission


class IsOrganizer(BasePermission):
    """Allow access only to users with organizer role."""

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_organizer


class IsAttendee(BasePermission):
    """Allow access only to non-organizer users."""

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_attendee

