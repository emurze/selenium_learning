import reprlib

from django.db import models


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
    photo = models.ImageField(upload_to='woman/%Y/%m/%d')
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created',)
        indexes = (
            models.Index(fields=('-created',)),
        )

    def __str__(self) -> str:
        return reprlib.repr(self.photo)