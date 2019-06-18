from django.db import models

from .choices import PLACE_TYPE


class Place(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=200, blank=True)
    type = models.CharField(choices=PLACE_TYPE, max_length=1)

    def __str__(self):
        return '{}-{}'.format(self.name, self.pk)
