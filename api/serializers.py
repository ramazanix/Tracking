from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Note, Theme
from .validators import validate_email as email_validator


class ThemesPkField(serializers.PrimaryKeyRelatedField):
    def get_queryset(self):
        user = self.context['request'].user
        if user.is_staff:
            return Theme.objects.all()
        return Theme.objects.filter(owner=user)


class NoteSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    themes = ThemesPkField(many=True)

    class Meta:
        model = Note
        fields = '__all__'


class ThemeSerializer(serializers.ModelSerializer):
    notes_list = NoteSerializer(many=True, read_only=True)
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Theme
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    notes = NoteSerializer(many=True, read_only=True)
    themes = ThemeSerializer(many=True, read_only=True)
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
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'notes', 'password', 'themes']
