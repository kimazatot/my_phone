from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from slugify import slugify

User = get_user_model()


class Brand(models.Model):
    slug = models.SlugField(primary_key=True, max_length=50, blank=True)
    name = models.CharField(max_length=100, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='brands')

    def __str__(self):
        return f'{self.name} --> {self.pk}'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save()

