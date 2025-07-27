from rest_framework.permissions import BasePermission


class OrganizerPermission(BasePermission):
    """Allow access only to authenticated organizers."""

    def has_permission(self, request, view):
        return request.user.is_authenticated and getattr(request.user, "is_organizer", False)
