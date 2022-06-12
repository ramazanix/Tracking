from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Note
from .validators import validate_email as email_validator


class NoteSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Note
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    notes = NoteSerializer(many=True, read_only=True)
    email = serializers.EmailField(min_length=10, max_length=100, required=True, validators=[email_validator])
    password = serializers.CharField(max_length=100, write_only=True)

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        user.save()
        return user

    def update(self, instance, validated_data):
        if 'password' in validated_data:
            password = validated_data.pop('password', instance.password)
            instance.set_password(password)
        return super().update(instance, validated_data)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'notes', 'password']
