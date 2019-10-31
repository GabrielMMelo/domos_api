from django.db import models

from device.models import Device


class Activity(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE)   
    state = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{} - {} - {}'.format(self.device, self.state, self.created_at)