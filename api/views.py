from rest_framework import generics, permissions
from .serializers import UserSerializer, NoteSerializer, ThemeSerializer
from .permissions import IsOwnerOrAdmin, IsUnauthorizedOrReadOnly, IsUserOrReadOnly
from .models import Note, Theme
from django.contrib.auth.models import User


class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsUnauthorizedOrReadOnly]


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsUserOrReadOnly]


class NoteList(generics.ListCreateAPIView):
    serializer_class = NoteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_staff:
            return Note.objects.all()
        return Note.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class NoteDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    permission_classes = [IsOwnerOrAdmin]
    lookup_field = 'slug'


class ThemeList(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ThemeSerializer

    def get_queryset(self):
        if self.request.user.is_staff:
            return Theme.objects.all()
        return Theme.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
