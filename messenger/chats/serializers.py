from rest_framework import serializers

from .models import Chat, Message, ChatMember


class ChatSerializer(serializers.ModelSerializer):
    chat = serializers.CharField(source='get_chat')

    class Meta:
        model = Chat


class MemberSerializer(serializers.ModelSerializer):
    chat = serializers.CharField(source='get_chat')

    class Meta:
        model = ChatMember


#####################################################


class MessageSerializer(serializers.ModelSerializer):
    chat = serializers.CharField(source='get_chat')
    sender = serializers.CharField(source='get_sender')

    class Meta:
        model = Message
        fields = ['id', 'content', 'chat', 'sender', 'created_at', 'is_forwarded', 'is_read']

