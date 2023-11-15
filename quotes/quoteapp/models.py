from django.db import models


# Create your models here.
class Authors(models.Model):
    fullname = models.CharField(max_length=100, null=False, unique=True)
    date_born = models.CharField(max_length=100, default='-')
    location_born = models.CharField(max_length=100, default='-')
    bio = models.CharField(default='-')


class Tag(models.Model):
    name = models.CharField(max_length=50, null=False, unique=True)


class Quotes(models.Model):
    tags = models.ManyToManyField(Tag)
    author = models.ForeignKey(Authors, on_delete=models.CASCADE, default=None, null=True)
    quote = models.CharField()
