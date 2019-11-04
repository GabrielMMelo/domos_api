import datetime
from django.db import models
from django.contrib.auth.models import User

from .choices import DEVICE_TYPE
from place.models import Place
import activity  # import deadlock with activity.models.Activity


class Device(models.Model):
    name = models.CharField(max_length=100)
    type = models.CharField(choices=DEVICE_TYPE, default="Generic", max_length=20)
    #TODO: place = models.ForeignKey(Place, on_delete=models.CASCADE)
    state = models.BooleanField(default=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    channel = models.CharField(max_length=200, blank=True)
    mac = models.CharField(max_length=17, unique=True)
    node_connected = models.BooleanField(default=False)

    def __str__(self):
        return '{} - {}'.format(self.name, self.mac)

    def get_updated_at(self):
        """ Get timestamp from last time state was updated """
        try:
            return activity.models.Activity.objects.filter(device=self.pk).last().created_at
        except:
            return datetime.datetime.now()

