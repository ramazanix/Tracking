from django.db import models
from django.urls import reverse
from pytils.translit import slugify


class Theme(models.Model):
    name = models.CharField(max_length=50)
    owner = models.ForeignKey('auth.User', related_name='themes', on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Note(models.Model):
    title = models.CharField(max_length=120)
    content = models.TextField(max_length=10000)
    owner = models.ForeignKey('auth.User', related_name='notes', on_delete=models.CASCADE)
    slug = models.SlugField(max_length=120, unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    themes = models.ManyToManyField(Theme, related_name='notes_list')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('note_detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            new_slug = slugify(self.title)
            self.slug = new_slug
        return super().save(*args, **kwargs)

    class Meta:
        ordering = ['created_at']
