import json

from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer

from .models import Device

class MyConsumer(AsyncWebsocketConsumer):
    groups = ["broadcast"]

    async def connect(self):
        # Called on connection.
        # To accept the connection call:
        await self.accept()

    async def receive(self, text_data=None, bytes_data=None):
        # Called with either text_data or bytes_data for each frame
        # You can call:
        await self.send(text_data="Hello world!")

    async def disconnect(self, close_code):
        # Called when the socket closes
        # Or add a custom WebSocket error code!
        await self.close(code=4123)

class DeviceConsumer(AsyncWebsocketConsumer):
    """
    """

    async def connect(self):
        self.device_id = self.scope['url_route']['kwargs'].get('id')  # pega o id da delivery
        self.device = Device.objects.get(pk=self.device_id)
        # self.user = self.scope["user"].username  # pega o usuário dono do ws
        # self.delivery = Delivery.objects.get(pk=self.delivery_id)  # recupera delivery do banco
        self.room_group_name = "device_" + self.device_id

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        await self.close()

    # Receive from websocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        status = text_data_json['status']

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'device.status',
                'status': device.status,
                'name': device.name,
            }
        )

    # Receive message from room group
    async def device_status(self, event):
        status = event['status']
        name = event['name']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': status,
            'from': name
        }))

        if status == 6:  # entrega cancelada
            await self.disconnect()
