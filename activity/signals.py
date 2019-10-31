from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Activity
from device.models import Device

@receiver(post_save, sender=Device)
def create_activity(sender, instance, created, **kwargs):
    if not created:
        first_activity = False 
        try:
            last_state = Activity.objects.filter(device=instance.pk).last().state
        except:
            first_activity = True

        if first_activity or not instance.state == last_state:
            activity = Activity()
            activity.device = Device.objects.filter(pk=instance.pk).first()
            activity.state = instance.state
            activity.save()