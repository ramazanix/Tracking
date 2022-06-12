from rest_framework.serializers import ValidationError
from django.contrib.auth.models import User


def validate_email(value):
    if User.objects.filter(email=value).exists():
        raise ValidationError(
            'User with this email is already exists.'
        )
