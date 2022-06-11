from django.contrib import admin
from .models import Note


class NoteAdmin(admin.ModelAdmin):
    list_display = ['title', 'content', 'owner']
    prepopulated_fields = {'slug': ('title',)}


admin.site.register(Note, NoteAdmin)
