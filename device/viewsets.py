import json

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from django.http import HttpResponse

from .models import Device
from .serializers import DeviceSerializer


class DeviceViewSet(ModelViewSet):
    serializer_class = DeviceSerializer

    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Device.objects.filter(owner=self.request.user)

    def create(self, request):
        user = request.user
        data = request.data

        try:
            device = Device.objects.get(owner=user, mac=data["mac"])
            return HttpResponse(json.dumps({"id": device.id}))
        except Device.DoesNotExist:
            data['owner'] = user
            device = Device(**data)
            device.save()
            return HttpResponse(json.dumps({'id': device.id}))

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
