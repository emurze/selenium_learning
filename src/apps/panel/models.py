import reprlib

from django.db import models


class Article(models.Model):
    title = models.CharField(max_length=128)
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
        return reprlib.repr(self.title)
