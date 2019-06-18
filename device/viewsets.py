import json

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet

from django.http import HttpResponse

from .models import Device
from .serializers import DeviceSerializer


class DeviceViewSet(ModelViewSet):
    serializer_class = DeviceSerializer

    # permission_classes = []

    def get_queryset(self):
        return Device.objects.all()

    @action(methods=['get'], detail=True, url_path='toggle', url_name='toggle')
    def toggle(self, request, pk=None):
        device = Device.objects.get(pk=pk)
        async_to_sync(get_channel_layer().send)(
            device.channel,
            {
                "type": "device.toggle",
                "state": int(not device.state),
            },
        )
        return HttpResponse(json.dumps({'status': 'ok'}))
