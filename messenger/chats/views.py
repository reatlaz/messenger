import redis
# from django.http import JsonResponse
from login_required import login_not_required
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_GET, require_POST, require_http_methods
from rest_framework import viewsets
from rest_framework.exceptions import ValidationError, PermissionDenied
from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from .models import Chat, Message, ChatMember
from users.models import User
from .serializers import ChatSerializer, ChatListSerializer, ChatUpdateSerializer
from .serializers import MessageSerializer, MessageUpdateSerializer, MessageMarkAsReadSerializer
from .serializers import MemberSerializer
from .tasks import send_email


class ChatViewSet(viewsets.ViewSet):
    # вопрос: стоит ли делать новый сериализатор для это вью?
    # вопрос: не мешают ли айди всего и вся из сериализаторов, которые используются в других вью?
    def list(self, request):
        chat_members = Chat.objects.filter(members__user=request.user.id)
        data = ChatListSerializer(chat_members, many=True).data
        return Response({'data': data})

    def create(self, request):
        serializer = ChatSerializer(data=request.data, context={'auth_user': request.user})
        serializer.is_valid(raise_exception=True)
        chat = serializer.save()
        return Response({'data': ChatSerializer(chat).data}, status=201)

    def retrieve(self, request, chat_id):
        try:
            ChatMember.objects.get(user=request.user, chat_id=chat_id)
        except ChatMember.DoesNotExist:
            raise PermissionDenied({"message": "You don't have access to this chat"})
        chat = get_object_or_404(Chat, id=chat_id)
        return Response({'data': ChatSerializer(chat).data})

    def update(self, request, chat_id):
        try:
            auth_usr = ChatMember.objects.get(user=request.user, chat_id=chat_id)
        except ChatMember.DoesNotExist:
            raise PermissionDenied({"message": "You don't have access to this chat or it doesn't exist"})
        if not (auth_usr.role == 'admin'):
            raise PermissionDenied({"message": "You don't have permission to alter this chat"})
        serializer = ChatUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # а можно как-то короче через save?
        chat = get_object_or_404(Chat, id=chat_id)
        chat = serializer.update(chat, serializer.validated_data)
        return Response({'data': ChatUpdateSerializer(chat).data})

    def destroy(self, request, chat_id):
        try:
            ChatMember.objects.get(user=request.user, chat_id=chat_id)
        except ChatMember.DoesNotExist:
            raise PermissionDenied({"message": "You don't have access to this chat"})
        chat = get_object_or_404(Chat, id=chat_id)
        chat.delete()
        return Response({})


class MessageViewSet(viewsets.ViewSet):

    def list(self, request, chat_id):
        try:
            ChatMember.objects.get(user=request.user, chat_id=chat_id)
        except ChatMember.DoesNotExist:
            raise PermissionDenied({"message": "You don't have access to this chat or it doesn't exist"})
        messages = Message.objects.filter(chat=chat_id)
        data = MessageSerializer(messages, many=True).data
        return Response({'data': data})

    def retrieve(self, request, message_id):
        try:
            message = get_object_or_404(Message, id=message_id)
            ChatMember.objects.get(user=request.user, chat_id=message.chat.id)
        except ChatMember.DoesNotExist:
            raise PermissionDenied({"message": "You don't have access to this chat or it doesn't exist"})

        return Response({'data': MessageSerializer(message).data})

    def create(self, request, chat_id):
        try:
            auth_usr = ChatMember.objects.get(user=request.user, chat_id=chat_id)
        except ChatMember.DoesNotExist:
            raise PermissionDenied({"message": "You don't have access to this chat or it doesn't exist"})
        serializer = MessageSerializer(data=request.data, context={'chat_id': chat_id, 'auth_usr': auth_usr})
        serializer.is_valid(raise_exception=True)
        message = serializer.save()
        return Response({'data': MessageSerializer(message).data}, status=201)

    def update(self, request, message_id):
        try:
            message = get_object_or_404(Message, id=message_id)
            auth_usr = ChatMember.objects.get(user=request.user, chat_id=message.chat.id)
        except ChatMember.DoesNotExist:
            raise PermissionDenied({"message": "You don't have access to this chat or it doesn't exist"})
        if not (auth_usr.role == 'admin'):
            raise PermissionDenied({"message": "You don't have permission to alter this chat"})
        serializer = MessageUpdateSerializer(
            data=request.data, context={'message_id': message_id})
        serializer.is_valid(raise_exception=True)
        # а можно как-то короче через save?
        message = get_object_or_404(Message, id=message_id)
        message = serializer.update(message, serializer.validated_data)
        return Response({'data': MessageSerializer(message).data})

    def partial_update(self, request, message_id):
        serializer = MessageMarkAsReadSerializer(
            data=request.data, context={'message_id': message_id})
        serializer.is_valid(raise_exception=True)
        # а можно как-то короче через save?
        message = get_object_or_404(Message, id=message_id)
        message = serializer.update(message, serializer.validated_data)
        return Response({'data': MessageSerializer(message).data})

    def destroy(self, request, message_id):
        message = get_object_or_404(Message, id=message_id)
        message.delete()
        return Response({})


class MemberViewSet(viewsets.ViewSet):

    def create(self, request, chat_id, user_id):
        usr = ChatMember.objects.get(user=request.user, chat_id=chat_id)
        if not(usr.role == 'admin'):
            raise PermissionDenied({"message": "You don't have permission to add users"})
        chat = get_object_or_404(Chat, id=chat_id)
        user = get_object_or_404(User, id=user_id)
        if ChatMember.objects.filter(user=user, chat=chat).exists():
            raise ValidationError("User already in the chat")
        else:
            member = ChatMember.objects.create(user=user, chat=chat)
            send_email(user.username, chat_id)
            data = MemberSerializer(member).data
            return Response({'data': data})

    def destroy(self, request, chat_id, user_id):
        usr = ChatMember.objects.get(user=request.user, chat_id=chat_id)
        if not (usr.role == 'admin'):
            raise PermissionDenied({"message": "You don't have permission to delete users"})
        chat = get_object_or_404(Chat, id=chat_id)
        user = get_object_or_404(User, id=user_id)
        member = get_object_or_404(ChatMember, user=user, chat=chat)
        member.delete()
        return Response({})


###################################################################


@require_GET
def index(request):
    return render(request, 'chats/index.html')


@require_GET
def home(request):
    return render(request, 'home.html')


@require_GET
@login_not_required
def login(request):
    r = redis.Redis()
    if r.exists('users_last_month'):
        users_last_month = int(r.get('users_last_month'))
    else:
        users_last_month = 0
    return render(request, 'login.html', {'users_last_month': users_last_month})









