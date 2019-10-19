import json

from rest_framework.authtoken.models import Token
from channels.db import database_sync_to_async
from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer

from .models import Device


class DeviceConsumer(AsyncWebsocketConsumer):
    @database_sync_to_async
    def get_device(self, **args):
        return Device.objects.get(**args)

    """
    @database_sync_to_async
    def set_mac(self, mac):
        self.device.mac = mac
        self.device.save()
    """

    @database_sync_to_async
    def update_state(self, state):
        self.device.state = state
        self.device.save()

    @database_sync_to_async
    def update_channel(self, channel):
        self.device.channel = channel
        self.device.save()

    async def connect(self):
        self.device_id = self.scope['url_route']['kwargs'].get(
            'id')  # pega o id da delivery
        self.device = await self.get_device(id=self.device_id)
        await self.update_channel(self.channel_name)
        self.device_room = str(self.device.id)

        await self.channel_layer.group_add(
            self.device_room, self.channel_name
        )  # one channel per device

        """
        await self.channel_layer.group_add(str(self.device.place),
            self.channel_name
        )  # one channel per place
        """

        # TODO: one channel for type?
        await self.accept()

    async def authorize(self, text_data_json={}):
        """ Check if given token is valid for any User and persist him in the scope """
        if self.scope['user'].id:
            return True

        try:
            token_key = text_data_json['token']
            token = Token.objects.get(key=token_key)
            self.scope['user'] = token.user
            return True
        except Exception as e:
            print("ERROR in authorize(): ", e)
            return False

    async def check_owner(self):
        """ Check if connection user is owner of the connection device """
        try:
            await self.get_device(id=self.device_id, owner=self.scope['user'])
            return True
        except Exception as e:
            return False

    async def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        authorized = await self.authorize(text_data_json)
        is_owner = await self.check_owner()
        
        if not authorized:
            await self.close()
            return
        
        if not is_owner:
            await self.close()
            return

        try:
            state = text_data_json['state']
            await self.update_state(state)  # is it needed?
            await self.channel_layer.group_send(self.device_room, {
                'type': 'device_broadcast',
                'state': state
            })
        except Exception as e:
            print("ERROR: ", e)

    # Receive message from room group
    async def device_broadcast(self, event):
        state = event['state']

        # Send message to WebSocket
        if await self.authorize():  # dont need to call check_owner() here
            await self.send(text_data=json.dumps({'state': state}))

    async def device_toggle(self, event):
        """ Handler for device.viewsets.toggle endpoint """
        await self.send(text_data=json.dumps({'state': event['state']}))

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name,
                                               self.channel_name)
        await self.close(code=1)
