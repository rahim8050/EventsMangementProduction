# rspvs/serializers.py
from rest_framework import serializers
from .models import RSVP


class RSVPSerializer(serializers.ModelSerializer):
    class Meta:
        model = RSVP
        fields = ("id", "user", "event", "approved", "created_at")
        read_only_fields = ("id", "user", "approved", "created_at")

    def validate(self, attrs):
        """
        - Prevent duplicate RSVPs for the same (user, event) early instead of
          letting the DB unique_together throw an IntegrityError.
        - (Optional) Enforce capacity here too, so errors come back as 400s from
          serializer validation; keep or drop depending on where you prefer it.
        """
        request = self.context.get("request")
        user = getattr(request, "user", None)
        event = attrs.get("event")

        if user and user.is_authenticated:
            # Duplicate RSVP guard
            if RSVP.objects.filter(user=user, event=event).exists():
                raise serializers.ValidationError("You have already RSVPed to this event.")

        # Capacity check (you can keep it only in the view if you prefer)
        if event and event.rsvps.filter(approved=True).count() >= event.max_attendees:
            raise serializers.ValidationError("Event capacity reached.")

        return attrs
