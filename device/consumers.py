import json

from channels.db import database_sync_to_async
from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer

from .models import Device

class DeviceConsumer(AsyncWebsocketConsumer):
    groups = ["broadcast"]

    @database_sync_to_async
    def get_device(self, id):
        return Device.objects.get(pk=id)

    @database_sync_to_async
    def update_device(self, state):
        self.device.state = state
        self.device.save()

    async def connect(self):
        self.device_id = self.scope['url_route']['kwargs'].get('id')  # pega o id da delivery
        self.device = await self.get_device(id=self.device_id)
        await self.channel_layer.group_add("device", self.channel_name)
        await self.accept()

    async def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        state = text_data_json['state']
        await self.update_device(state)
        await self.send(text_data=self.device.state)

    async def device_toggle(self, event):
        """Handler for device.viewsets toggle endpoint"""
        await self.send(text_data=json.dumps({'state': event['state'], 'device': event['device']}))

    async def disconnect(self, close_code):
        await self.close(code=4123)
