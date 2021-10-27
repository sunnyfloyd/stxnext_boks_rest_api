from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.core.validators import MinValueValidator, MaxValueValidator


class Book(models.Model):
    id = models.CharField(max_length=20, primary_key=True)
    title = models.CharField(max_length=120)
    authors = ArrayField(models.CharField(max_length=120), blank=True, default=list)
    published_date = models.DateField()
    categories = ArrayField(models.CharField(max_length=120), blank=True, default=list)
    average_rating = models.FloatField(
        validators=[MinValueValidator(0)], blank=True, null=True
    )
    ratings_count = models.IntegerField(
        validators=[MinValueValidator(0)], blank=True, null=True
    )
    thumbnail = models.URLField(blank=True)
