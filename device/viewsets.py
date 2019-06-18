from rest_framework.viewsets import ModelViewSet

from .models import Device
from .serializers import DeviceSerializer


class DeviceViewSet(ModelViewSet):
    """
    A simple ViewSet for viewing and editing accounts.
    """
    serializer_class = DeviceSerializer
    # permission_classes = [IsAccountAdminOrReadOnly]

    def get_queryset(self):
        return Device.objects.all()
