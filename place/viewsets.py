from rest_framework.viewsets import ModelViewSet

from .models import Place
from .serializers import PlaceSerializer


class PlaceViewSet(ModelViewSet):
    """
    A simple ViewSet for viewing and editing accounts.
    """
    serializer_class = PlaceSerializer
    # permission_classes = [IsAccountAdminOrReadOnly]

    def get_queryset(self):
        return Place.objects.all()
