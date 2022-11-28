import json
# from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_GET, require_POST, require_http_methods
from rest_framework import viewsets
from rest_framework.response import Response
# from rest_framework.generics import RetrieveUpdateDestroyAPIView

from .models import Chat, Message, ChatMember
from users.models import User
from .serializers import ChatSerializer, MessageSerializer, MemberSerializer


class ChatViewSet(viewsets.ViewSet):
    # валидация в сериалайзере ValidationError
    # сделать максимально короткие view
    def list(self, request, user_id):
        chat_members = ChatMember.objects.filter(user=user_id)
        data = []
        for member in chat_members:
            chat = ChatSerializer(member.chat).data
            try:
                last_message_object = Message.objects.filter(chat=member.chat).latest('created_at')
                last_message = MessageSerializer(last_message_object).data
            except Message.DoesNotExist:
                last_message = None
            chat['last_message'] = last_message
            data.append(chat)
        return Response({'data': data})

    def create(self, request):
        #  validate serializer для получения данных
        chat_name = request.POST.get('chat_name', 'New chat')
        chat_description = request.POST.get('description', '')
        user_ids = [int(str_user_id) for str_user_id in request.POST.getlist('user_ids')]
        chat = Chat.objects.create(name=chat_name, description=chat_description)
        # chat.save()
        for user_id in user_ids:
            user = get_object_or_404(User, id=user_id)
            member = ChatMember.objects.create(user=user, chat=chat)
            member.save()
        # data = ChatSerializer(chat).data
        return Response({'data': chat.id}, status=201)

    def retrieve(self, request, chat_id):
        chat = get_object_or_404(Chat, id=chat_id)
        data = ChatSerializer(chat).data
        return Response({'data': data})

    def update(self, request, chat_id):
        chat = get_object_or_404(Chat, id=chat_id)
        json_data = json.loads(request.body)
        chat.name = json_data.get('name', chat.name)
        chat.description = json_data.get('description', chat.description)
        chat.save()
        return Response({
            'data':
                {
                    'id': chat.id,
                    'name': chat.name,
                    'description': chat.description,
                },
            })

    def destroy(self, request, chat_id):
        chat = get_object_or_404(Chat, id=chat_id)
        chat.delete()
        return Response({})


class MessageViewSet(viewsets.ViewSet):

    def list(self, request, chat_id):
        messages = Message.objects.filter(chat=chat_id)
        response_data = MessageSerializer(messages, many=True).data
        return Response({'messages': response_data})

    def retrieve(self, request, message_id):
        message = get_object_or_404(Message, id=message_id)
        data = MessageSerializer(message).data
        return Response({'data': data})

    def create(self, request, chat_id):
        message_content = request.POST.get('content')
        user_id = request.POST.get('user_id')
        sender = get_object_or_404(ChatMember, chat=chat_id, user=user_id)
        message = Message.objects.create(content=message_content, sender=sender, chat=sender.chat)
        message.save()
        return Response({'new_message_id': message.id}, status=201)

    def update(self, request, message_id):
        message = get_object_or_404(Message, id=message_id)
        json_data = json.loads(request.body)
        message.content = json_data.get('content', message.content)
        message.save()
        return Response({
            'edited_message':
                {
                    'content': message.content,
                    'chat': message.chat.id,
                    'sender': message.sender.user.id,
                    'created_at': message.created_at,
                    'is_forwarded': message.is_forwarded,
                },
        })

    def partial_update(self, request, message_id):
        message = get_object_or_404(Message, id=message_id)
        message.is_read = True
        message.save()
        return Response({
            'message_marked_as_read':
                {
                    'id': message.id
                }
        })

    def destroy(self, request, message_id):
        message = get_object_or_404(Message, id=message_id)
        message.delete()
        return Response({})


# class AddRemoveMember(RetrieveUpdateDestroyAPIView):
#    serializer_class = MemberSerializer


class MemberViewSet(viewsets.ViewSet):

    def create(self, request, chat_id, user_id):   # 3 to be tested
        chat = get_object_or_404(Chat, id=chat_id)
        user = get_object_or_404(User, id=user_id)
        member = ChatMember.objects.get_or_create(user=user, chat=chat)

        return Response({
            'data': {
                'id': member.id,
            }
        }, status=201)

    def destroy(self, request, chat_id, user_id):  # 4 to be tested
        chat = get_object_or_404(Chat, id=chat_id)
        user = get_object_or_404(User, id=user_id)
        member = get_object_or_404(ChatMember, user=user, chat=chat)
        member.delete()
        return Response({})


###################################################################


@require_GET
def index(request):
    return render(request, 'chats/index.html')







