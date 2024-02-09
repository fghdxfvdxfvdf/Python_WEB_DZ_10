from django.db import models


class Authors(models.Model):
    author = models.CharField(max_length=150)
    borns = models.CharField(max_length=150)
    borns_location = models.CharField(max_length=200)
    descriptions = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class Tag(models.Model):
    name = models.CharField(max_length=50, null=False, unique=True)


class Quotes(models.Model):
    quote = models.TextField()
    tags = models.ManyToManyField(Tag)
    author = models.ForeignKey(
        Authors, on_delete=models.CASCADE, default=None, null=False
    )
    created_at = models.DateTimeField(auto_now_add=True)
