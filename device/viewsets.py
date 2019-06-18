from django.http import HttpResponse

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet

from .models import Device
from .serializers import DeviceSerializer


class DeviceViewSet(ModelViewSet):
    serializer_class = DeviceSerializer
    # permission_classes = []

    def get_queryset(self):
        return Device.objects.all()

    # TODO: Alterar endpoint para extrair o id do device pelo usuário atual e não pela URL
    @action(methods=['get'], detail=True,
            url_path='toggle', url_name='toggle')
    def toggle(self, request, pk=None):
        async_to_sync(get_channel_layer().group_send)(
            "device",
            {
                "type": "device.toggle",
                "state": int(not Device.objects.get(pk=pk).state),
                "device": pk,
            },
        )
        return HttpResponse("ok")
