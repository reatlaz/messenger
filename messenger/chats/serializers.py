from rest_framework import serializers

from .models import Chat, Message, ChatMember


class ChatSerializer(serializers.ModelSerializer):

    class Meta:
        model = Chat
        fields = ['id', 'name', 'description']


class ChatListSerializer(serializers.ModelSerializer):
    chat = serializers.CharField(source='get_chat')
    sender = serializers.CharField(source='get_sender')

    class Meta:
        model = Message
        fields = ['id', 'name', 'last_message']


class MemberSerializer(serializers.ModelSerializer):
    chat = serializers.CharField(source='get_chat')

    class Meta:
        model = ChatMember
        fields = ['id', 'chat', 'user']


#####################################################


class MessageSerializer(serializers.ModelSerializer):
    # chat = serializers.CharField(source='get_chat')
    sender = serializers.CharField(source='get_sender')

    class Meta:
        model = Message
        fields = ['id', 'content', 'sender', 'created_at', 'is_forwarded', 'is_read']

