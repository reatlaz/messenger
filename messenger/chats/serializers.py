from django.shortcuts import get_object_or_404

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import Chat, Message, ChatMember
from users.models import User
from users.serializers import UserSerializer


class MemberSerializer(serializers.ModelSerializer):

    class Meta:
        model = ChatMember
        fields = ['id', 'user', 'role']


class ChatSerializer(serializers.ModelSerializer):
    members = MemberSerializer(many=True, write_only=True, required=False)

    class Meta:
        model = Chat
        fields = ['id', 'name', 'description', 'members', 'is_private']

    def create(self, validated_data):
        members = validated_data.pop('members', [])
        chat = Chat.objects.create(**validated_data)
        for member_dict in members:
            member_dict['chat'] = chat
            ChatMember.objects.create(**member_dict)
        ChatMember.objects.create(user=self.context['auth_user'], chat=chat, role='admin')
        return chat


class ChatUpdateSerializer(serializers.ModelSerializer):

    members = MemberSerializer(many=True, write_only=True, required=False)
    name = serializers.CharField(required=False)
    description = serializers.CharField(required=False)

    class Meta:
        model = Chat
        fields = ['id', 'name', 'description', 'members']

    def update(self, chat, validated_data):
        chat.name = validated_data.get('name', chat.name)
        chat.description = validated_data.get('description', chat.description)
        members = validated_data.pop('members', [])
        for member_dict in members:
            member_dict['chat'] = chat
            ChatMember.objects.create(**member_dict)
        chat.save()
        return chat
#############################################################################


class MessageSerializer(serializers.ModelSerializer):
    content = serializers.CharField(allow_blank=True)
    image = serializers.URLField(required=False, allow_blank=True)
    audio = serializers.URLField(required=False, allow_blank=True)
    sender = serializers.CharField(source='get_sender', required=False)

    class Meta:
        model = Message
        fields = ['id', 'content', 'sender', 'created_at', 'image', 'audio', 'is_forwarded', 'is_read']

    def create(self, validated_data):
        chat_id = self.context['chat_id']
        auth_usr = self.context['auth_usr']
        chat = get_object_or_404(Chat, id=chat_id)
        message = Message.objects.create(chat=chat, sender=auth_usr, **validated_data)

        return message


class MessageUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Message
        fields = ['id', 'content', 'sender', 'created_at', 'image', 'is_forwarded', 'is_read']

    def update(self, message, validated_data):
        message.content = validated_data['content']
        message.save()
        return message


class MessageMarkAsReadSerializer(serializers.ModelSerializer):

    class Meta:
        model = Message
        fields = []

    def update(self, message, validated_data):
        message.is_read = True
        message.save()
        return message
#############################################################################


class ChatListSerializer(serializers.ModelSerializer):
    # chat = serializers.CharField(source='get_chat')
    # sender = serializers.CharField(source='get_sender')
    last_message = MessageSerializer(source='get_last_message')

    class Meta:
        model = Chat
        fields = ['id', 'name', 'last_message', 'is_private']