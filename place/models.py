from django.db import models

from .choices import PLACE_TYPE

# Create your models here.
class Place(models.Model):
    name = models.CharField(max_length=50)
    type = models.CharField(choices=PLACE_TYPE, max_length=1)
