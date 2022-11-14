import json
from django.http import JsonResponse, QueryDict
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_GET, require_POST, require_http_methods

from .models import Chat, Message, ChatMember
from users.models import User


@require_GET
def index(request):
    return render(request, 'chats/index.html')


@require_POST  # 1 готово
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
    return JsonResponse({'new_chat_id': chat.id})


@require_http_methods(['PUT'])  # 2 готово
def edit_chat(request, chat_id):
    chat = get_object_or_404(Chat, id=chat_id)
    json_data = json.loads(request.body)
    chat.name = json_data.get('name', chat.name)
    chat.description = json_data.get('description', chat.description)
    chat.save()
    return JsonResponse({
        'edited_chat':
            {
                'name': chat.name,
                'description': chat.description,
            },
        })


@require_http_methods(['PUT'])  # 3 to be tested
def add_member_to_chat(request, chat_id, user_id):
    chat = get_object_or_404(Chat, id=chat_id)
    user = get_object_or_404(User, id=user_id)
    member = ChatMember.objects.create(user=user, chat=chat)
    member.save()
    return JsonResponse({
        'user_added_to_chat': {
            'user_id': user.id,
            'chat_id': chat.id,
        }
    })


@require_http_methods(['DELETE'])  # 4 to be tested
def delete_member_from_chat(request, chat_id, user_id):
    chat = get_object_or_404(Chat, id=chat_id)
    user = get_object_or_404(User, id=user_id)
    member = get_object_or_404(ChatMember, user=user, chat=chat)
    member.delete()
    return JsonResponse({
        'user_deleted_from_chat': {
            'user_id': user.id,
            'chat_id': chat.id,
        }
    })


@require_http_methods(['DELETE'])  # 5 готово
def delete_chat(request, chat_id):
    chat = get_object_or_404(Chat, id=chat_id)
    chat.delete()
    return JsonResponse({'deleted_chat_id': chat_id})


@require_POST  # 6 to be tested
def create_message(request, chat_id):
    message_content = request.POST.get('content')
    user_id = request.POST.get('user_id')
    sender = get_object_or_404(ChatMember, chat=chat_id, user=user_id)
    message = Message.objects.create(content=message_content, sender=sender, chat=sender.chat)
    message.save()

    return JsonResponse({'new_message_id': message.id})


@require_http_methods(['PUT'])  # 7 готово
def edit_message(request, message_id):
    message = get_object_or_404(Message, id=message_id)
    json_data = json.loads(request.body)
    message.content = json_data.get('content', message.content)
    message.save()
    return JsonResponse({
        'edited_message':
            {
                'content': message.content,
                'chat': message.chat.id,
                'sender': message.sender.user.id,
                'created_at': message.created_at,
                'is_forwarded': message.is_forwarded,
                'is_read': message.is_read,
            },
        })


@require_http_methods(['PUT'])  # 8 to be tested
def mark_message_as_read(request, message_id):
    message = get_object_or_404(Message, id=message_id)
    message.is_read = True
    message.save()
    return JsonResponse({
        'message_marked_as_read':
            {
                'id': message.id
            }
    })


@require_http_methods(['DELETE'])  # 9 готово
def delete_message(request, message_id):
    message = get_object_or_404(Message, id=message_id)
    message.delete()
    return JsonResponse({'deleted_message_id': message_id})


@require_GET  # 10 готово
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
    return JsonResponse({'chats': response_data})


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
    return JsonResponse({'messages': response_data})


@require_GET  # 13 готово
def chat_detail(request, chat_id):
    chat = get_object_or_404(Chat, id=chat_id)
    return JsonResponse({
        'name': chat.name,
        'description': chat.description,
    })


@require_GET  # 14 готово
def message_detail(request, message_id):
    message = get_object_or_404(Message, id=message_id)
    return JsonResponse({
        'id': message.id,
        'content': message.content,
        'chat': message.chat.id,
        'sender': message.sender.user.id,
        'created_at': message.created_at,
        'is_forwarded': message.is_forwarded,
        'is_read': message.is_read,
    })



