from rest_framework import serializers

from .models import Chat, Message


class MessageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Message
        fields = ['content', 'created_at', 'is_forwarded', 'is_read', ]
