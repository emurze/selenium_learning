import reprlib

from django.db import models
from django.db.models import Q


class Article(models.Model):
    href = models.CharField(unique=True, max_length=512)
    src = models.CharField(unique=True, max_length=512)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created',)
        indexes = (
            models.Index(fields=('-created',)),
            models.Index(fields=('href',)),
            models.Index(fields=('src',)),
        )

    def __str__(self) -> str:
        return reprlib.repr(self.src)


class Woman(models.Model):
    url = models.CharField(max_length=1012, null=True)
    photo = models.ImageField(upload_to='woman/%Y/%m/%d')
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created',)
        indexes = (
            models.Index(fields=('-created',)),
            models.Index(
                name='woman_url_is_not_null_index',
                fields=('url',),
                condition=Q(url__isnull=False),
            )
        )

    def __str__(self) -> str:
        return reprlib.repr(self.photo)