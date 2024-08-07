from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import json
from django.utils import timezone
from .models import UserActivity
from .utils import translate

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Получение языка из URL-параметров
        self.user_language = self.scope['query_string'].decode().split('language=')[1] if 'language=' in self.scope['query_string'].decode() else 'en'
        print("User language:", self.user_language)

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        user = self.scope['user']

        if user.is_authenticated:
            UserActivity.objects.create(
                user=user,
                room_name=self.room_name,
                message=message,
                timestamp=timezone.now()
            )
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'user': str(user),
                'user_language': self.user_language,
            }
        )
    def chat_message(self, event):
        message = event['message']
        user = event['user']
        user_language = event['user_language']

        translated_message = translate(user_language, message)

        # Переводим сообщение на язык пользователя
        self.send(text_data=json.dumps({
            'event': "Send",
            'message': translated_message,
            'user': user,
        }))

