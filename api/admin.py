from django.contrib import admin
from .models import Note, Theme


class NoteAdmin(admin.ModelAdmin):
    list_display = ['title', 'content', 'owner']
    prepopulated_fields = {'slug': ('title',)}


class ThemeAdmin(admin.ModelAdmin):
    list_display = ['name', 'owner']


admin.site.register(Note, NoteAdmin)
admin.site.register(Theme, ThemeAdmin)
