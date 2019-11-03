from rest_framework import serializers

from .models import Device


class DeviceSerializer(serializers.ModelSerializer):
    updated_at = serializers.CharField(source='get_updated_at')

    class Meta:
        model = Device
        fields = '__all__'
        read_only_fields = ('channel', 'updated_at')