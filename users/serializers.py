from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    username = serializers.CharField(required=False)

    class Meta:
        model = User
        fields = ("id", "username", "email", "password", "role")
        extra_kwargs = {
            "email": {"required": True},
            "role": {"required": False}
        }

    def validate(self, attrs):
        """Validate email and username for uniqueness."""
        email = attrs.get("email")
        username = attrs.get("username") or email  # default to email if not provided

        errors = {}

        # Check email uniqueness
        if User.objects.filter(email=email).exists():
            errors["email"] = ["This email is already registered."]

        # Check username uniqueness
        if User.objects.filter(username=username).exists():
            errors["username"] = ["This username is already taken."]

        if errors:
            raise serializers.ValidationError(errors)

        attrs["username"] = username
        return attrs

    def create(self, validated_data):
        """Create user with a hashed password."""
        password = validated_data.pop("password")
        user = User.objects.create_user(password=password, **validated_data)
        return user


class EmailAuthTokenSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, trim_whitespace=False)

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        if not email or not password:
            raise serializers.ValidationError('Must include "email" and "password".')

        # Step 1: Find user by email
        try:
            user_obj = User.objects.get(email=email)
        except User.DoesNotExist:
            raise AuthenticationFailed("Unable to log in with provided credentials.")

        # Step 2: Authenticate using the associated username
        user = authenticate(username=user_obj.username, password=password)

        if not user:
            raise AuthenticationFailed("Unable to log in with provided credentials.")

        if not user.is_active:
            raise AuthenticationFailed("User account is disabled.")

        attrs["user"] = user
        return attrs