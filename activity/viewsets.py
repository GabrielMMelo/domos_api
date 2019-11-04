import json
from datetime import datetime, timedelta

from django.http import HttpResponse
from django.db.models import Count
from django.utils import timezone
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response

from device.models import Device
from .models import Activity
from .serializers import ActivitySerializer


class ActivityViewSet(ModelViewSet):
    serializer_class = ActivitySerializer

    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        devices = Device.objects.filter(owner=self.request.user)
        return Activity.objects.filter(device__in=devices)

    @action(methods=['get'], detail=False, url_path='biggest_uptime_last_month', url_name='biggest_uptime_last_month')
    def biggest_uptime_last_month(self, request):
        last_30_days = datetime.today() - timedelta(days=30)
        devices = Device.objects.filter(owner=self.request.user)

        response = {
            'series': [],
            'labels': [],
        }

        for device in devices:
            total_uptime = 0.0
            last_time_on = None
            last_activity_state = None
            activities = Activity.objects.filter(device=device, created_at__gte=last_30_days)
            for activity in activities:
                if activity.state:
                    if last_activity_state:
                        continue
                    last_activity_state = True
                    last_time_on = activity.created_at
                elif last_time_on is not None:
                    if not last_activity_state:
                        continue
                    last_activity_state = False
                    total_uptime += (activity.created_at - last_time_on).seconds

            if last_activity_state:
                total_uptime += (timezone.now() - last_time_on).seconds

            hours, remainder = divmod(total_uptime, 3600)
            minutes, _ = divmod(remainder, 60)
            total_uptime_str =  float('{:02}.{:02}'.format(int(hours), int(minutes)))  # hours.minutes
            response['series'].append(total_uptime_str),
            response['labels'].append(device.name),

        return HttpResponse(json.dumps({'activities': response}))

    @action(methods=['get'], detail=False, url_path='most_switched_last_month', url_name='most_switched_last_month')
    def most_switched_last_month(self, request):

        last_30_days = datetime.today() - timedelta(days=30)
        devices = Device.objects.filter(owner=self.request.user)
        activities = Activity.objects.filter(device__in=devices, created_at__gte=last_30_days)
        # uses pk to get Count
        devices = Device.objects.filter(activity__in=activities).annotate(num_activities=Count('activity'))

        response = {
            'series': [],
            'labels': [],
        }

        for device in devices:
            response['series'].append(device.num_activities),
            response['labels'].append(device.name),

        return HttpResponse(json.dumps({'activities': response}))
