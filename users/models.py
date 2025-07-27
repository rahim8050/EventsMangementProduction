from django.contrib.auth.models import AbstractUser
from django.db import models
import roles


class User(AbstractUser):
    """Custom user model that stores a role."""

    role = models.CharField(
        max_length=20,
        choices=roles.ROLE_CHOICES,
        default=roles.DEFAULT_ROLE,
    )

    def __str__(self) -> str:  # pragma: no cover - convenience
        return self.email or self.username

    @property
    def is_organizer(self) -> bool:
        return self.role == roles.ORGANIZER

    @property
    def is_attendee(self) -> bool:
        return self.role == roles.ATTENDEE
