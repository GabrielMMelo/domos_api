from django.db import models

from .choices import DEVICE_TYPE
from place.models import Place


class Device(models.Model):
    name = models.CharField(max_length=100)
    type = models.CharField(choices=DEVICE_TYPE, max_length=1)
    place = models.ForeignKey(Place, on_delete=models.CASCADE)
    state = models.BooleanField(default=False)
    channel = models.CharField(max_length=200, blank=True)
    mac = models.CharField(max_length=17, blank=True, unique=True)

    def __str__(self):
        return '{} - {}'.format(self.name, self.place)
