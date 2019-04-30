# !/usr/bin/env python
# -*- coding: utf-8 -*-
# chat/consumers.py
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django.conf import settings
import random
import time
import json
SIGNAL = settings.WEBSOCKET_SIGNAL


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        print('connect1')

        self.accept()
        print('connect2')

    def disconnect(self, close_code):
        # Leave room group
        try:
            async_to_sync(self.channel_layer.group_discard)(
                self.room_group_name,
                self.channel_name
            )
        except Exception as e:
            print(e)

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        signal = SIGNAL.get(message)
        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': signal,
                'message': message
            }
        )

    # Receive message from room group
    def send_message(self, event):
        message = event['message']
        if message.upper() == 'READY':
            print('1')
            while True:
                time.sleep(0.2)
                value = [random.randint(20, 30), random.randint(20, 30),
                         random.randint(20, 30), random.randint(20, 30),
                         random.randint(20, 30)]
            # Send message to WebSocket
            # Send message to WebSocket
                self.send(text_data=json.dumps({
                    'series_value': value
                }))

    def kill_websocket(self, event):
        pass

