from rest_framework import serializers

from .models import Chat, Message


class MessageSerializer(serializers.ModelSerializer):
    chat = serializers.CharField(source='get_chat')

    class Meta:
        model = Message
        fields = ['content', 'created_at', 'is_forwarded', 'is_read', 'chat']


#class ChatSerializer(serializers.ModelSerializer):
