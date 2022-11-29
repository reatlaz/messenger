import json
# from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_GET, require_POST, require_http_methods
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from .models import Chat, Message, ChatMember
from users.models import User
from .serializers import ChatSerializer, ChatListSerializer, MessageSerializer, MemberSerializer


class ListCreateChat(ListCreateAPIView):
    serializer_class = ChatSerializer
    queryset = Chat.objects.all()

    def list(self, request, user_id):
        chat_members = ChatMember.objects.filter(user=user_id)
        data = []
        for member in chat_members:
            chat = ChatListSerializer(member.chat).data
            data.append(chat)
        return Response({'data': data})

class ChatViewSet(viewsets.ViewSet):
    # валидация в сериалайзере ValidationError
    # сделать максимально короткие view
    # вопрос: стоит ли делать новый сериализатор для это вью?
    # вопрос: не мешают ли айди всего и вся из сериализаторов, которые используются в других вью?
    def list(self, request, user_id):
        chat_members = ChatMember.objects.filter(user=user_id)
        data = []
        for member in chat_members:
            chat = ChatListSerializer(member.chat).data
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
        data = ChatSerializer(chat).data
        return Response({'data': data}, status=201)

    def retrieve(self, request, chat_id):
        chat = get_object_or_404(Chat, id=chat_id)
        data = ChatSerializer(chat).data
        return Response({'data': data})

    def update(self, request, chat_id):
        chat = get_object_or_404(Chat, id=chat_id)
        request_json = json.loads(request.body)
        chat.name = request_json.get('name', chat.name)
        chat.description = request_json.get('description', chat.description)
        chat.save()
        data = ChatSerializer(chat).data
        return Response({'data': data})

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







