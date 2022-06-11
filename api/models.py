from django.db import models
from django.urls import reverse
from pytils.translit import slugify


class Note(models.Model):
    title = models.CharField(max_length=120)
    content = models.TextField(max_length=10000)
    owner = models.ForeignKey('auth.User', related_name='notes', on_delete=models.CASCADE)
    slug = models.SlugField(max_length=120, unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('note_detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

    class Meta:
        ordering = ['created_at']
