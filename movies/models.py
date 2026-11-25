from django.db import models


class Genre(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Movie(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    duration = models.IntegerField()
    release_date = models.DateField()
    poster_url = models.URLField()
    genres = models.ManyToManyField(Genre)

    def __str__(self):
        return self.title
