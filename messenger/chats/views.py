import json
from django.http import JsonResponse, QueryDict
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_GET, require_POST, require_http_methods

from .models import Chat, Message, ChatMember
from users.models import User


@require_GET
def index(request):
    return render(request, 'chats/index.html')


@require_POST  # 1
def create_chat(request):
    chat_name = request.POST.get('chat_name', 'New chat')
    chat_description = request.POST.get('description', '')
    user_ids = [int(str_user_id) for str_user_id in request.POST.getlist('user_ids')]
    chat = Chat.objects.create(name=chat_name, description=chat_description)
    chat.save()
    for user_id in user_ids:
        user = get_object_or_404(User, id=user_id)
        member = ChatMember.objects.create(user=user, chat=chat)
        member.save()
    return JsonResponse({'data': chat.id})


@require_http_methods(['PUT'])  # 2
def edit_chat(request, chat_id):
    chat = get_object_or_404(Chat, id=chat_id)
    json_data = json.loads(request.body)
    chat.name = json_data.get('name', chat.name)
    chat.description = json_data.get('description', chat.description)
    chat.save()
    return JsonResponse({
        'data':
            {
                'id': chat_id,
                'name': chat.name,
                'description': chat.description,
            },
        })


@require_http_methods(['PUT'])  # 3
def add_member_to_chat(request, chat_id, user_id):
    chat = get_object_or_404(Chat, id=chat_id)
    user = get_object_or_404(User, id=user_id)
    member = ChatMember.objects.get_or_create(user=user, chat=chat)
    return JsonResponse({'data': member.id})


@require_http_methods(['DELETE'])  # 4
def delete_member_from_chat(request, chat_id, user_id):
    chat = get_object_or_404(Chat, id=chat_id)
    user = get_object_or_404(User, id=user_id)
    member = get_object_or_404(ChatMember, user=user, chat=chat)
    member.delete()
    return JsonResponse({})


@require_http_methods(['DELETE'])  # 5
def delete_chat(request, chat_id):
    chat = get_object_or_404(Chat, id=chat_id)
    chat.delete()
    return JsonResponse({})


@require_POST  # 6
def create_message(request, chat_id):
    message_content = request.POST.get('content')
    user_id = request.POST.get('user_id')
    sender = get_object_or_404(ChatMember, chat=chat_id, user=user_id)
    message = Message.objects.create(content=message_content, sender=sender, chat=sender.chat)
    # просто message_id, или, например, везде ключ 'data'
    return JsonResponse({'data': message.id})


@require_http_methods(['PUT'])  # 7
def edit_message(request, message_id):
    message = get_object_or_404(Message, id=message_id)
    json_data = json.loads(request.body)
    message.content = json_data.get('content', message.content)
    message.save()
    return JsonResponse({
        'data':
            {
                'content': message.content,
                'chat': message.chat.id,
                'sender': message.sender.user.id,
                'created_at': message.created_at,
                'is_forwarded': message.is_forwarded,
                'is_read': message.is_read,
            },
        })


@require_http_methods(['PUT'])  # 8
def mark_message_as_read(request, message_id):
    message = get_object_or_404(Message, id=message_id)
    message.is_read = True
    message.save()
    return JsonResponse({})


@require_http_methods(['DELETE'])  # 9
def delete_message(request, message_id):
    message = get_object_or_404(Message, id=message_id)
    message.delete()
    return JsonResponse({})


@require_GET  # 10
def chat_list(request, user_id):
    chat_members = ChatMember.objects.filter(user=user_id)
    response_data = []
    for member in chat_members:
        last_message = Message.objects.filter(chat=member.chat).latest('created_at')
        response_data.append({
            'id': member.chat.id,
            'name': member.chat.name,
            'last_message_text': last_message.content if last_message else '',
            'last_message_time': last_message.created_at if last_message else '',
        })
    return JsonResponse({'data': response_data})


@require_GET  # 11
def message_list(request, chat_id):
    messages = Message.objects.filter(chat=chat_id)
    response_data = []
    for message in messages:
        response_data.append({
            'content': message.content,
            'sender': message.sender.user.id,
            'created_at': message.created_at,

        })
    return JsonResponse({'data': response_data})


@require_GET  # 13
def chat_detail(request, chat_id):
    chat = get_object_or_404(Chat, id=chat_id)
    return JsonResponse({
        'data': {
            'name': chat.name,
            'description': chat.description,
        }
    })


@require_GET  # 14
def message_detail(request, message_id):
    message = get_object_or_404(Message, id=message_id)
    return JsonResponse({
        'data': {
            'id': message.id,
            'content': message.content,
            'chat': message.chat.id,
            'sender': message.sender.user.id,
            'created_at': message.created_at,
            'is_forwarded': message.is_forwarded,
            'is_read': message.is_read,
        }
    })



