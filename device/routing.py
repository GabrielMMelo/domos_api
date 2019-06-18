from django.urls import path

from . import consumers

device_urlpatterns = [
    path('ws/device/<id>/', consumers.DeviceConsumer),
]
