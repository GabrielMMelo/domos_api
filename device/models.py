from django.db import models
from django.contrib.auth.models import User

from .choices import DEVICE_TYPE
from place.models import Place


class Device(models.Model):
    name = models.CharField(max_length=100)
    type = models.CharField(choices=DEVICE_TYPE, default="Generic", max_length=20)
    #TODO: place = models.ForeignKey(Place, on_delete=models.CASCADE)
    state = models.BooleanField(
        default=False
    )
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    channel = models.CharField(max_length=200, blank=True)
    mac = models.CharField(max_length=17, unique=True)

    def __str__(self):
        return '{} - {}'.format(self.name, self.mac)
