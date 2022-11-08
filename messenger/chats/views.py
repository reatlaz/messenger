import json
from django.http import JsonResponse, QueryDict
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_GET, require_POST, require_http_methods

from .models import Chat, Message, ChatMember
from users.models import User


@require_GET
def index(request):
    return render(request, 'chats/index.html')


@require_GET
def chat_list(request, user_id):
    chat_members = ChatMember.objects.filter(user=user_id)

    response_data = []
    for member in chat_members:
        try:
            last_message = Message.objects.filter(chat=member.chat).latest('created_at')
            last_message_content = last_message.content
            last_message_created_at = last_message.created_at
        except Message.DoesNotExist:
            last_message_content = None
            last_message_created_at = None

        response_data.append({
            'id': member.chat.id,
            'name': member.chat.name,
            'last_message_text': last_message_content,
            'last_message_time': last_message_created_at,
        })
    return JsonResponse({'chats': response_data})


@require_GET
def chat_detail(request, chat_id):
    chat = get_object_or_404(Chat, id=chat_id)
    print(chat)
    return JsonResponse({
        'name': chat.name,
        'description': chat.description,
    })


@require_POST
def create_chat(request):
    # print(request.body)
    chat_name = request.POST.get('chat_name')
    user_ids = [int(str_user_id) for str_user_id in request.POST.getlist('user_ids[]')]
    # print(request.POST)
    # print(user_ids)
    chat = Chat.objects.create(name=chat_name)
    chat.save()
    for user_id in user_ids:
        user = User.objects.get(id=user_id)
        member = ChatMember.objects.create(user=user, chat=chat)
        member.save()
    return JsonResponse({'new_chat_id': chat.id})


@require_http_methods(['PUT'])
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


@require_http_methods(['DELETE'])
def delete_chat(request, chat_id):
    chat = get_object_or_404(Chat, id=chat_id)
    chat.delete()

    return JsonResponse({'deleted_chat_id': chat_id})

###############################################


@require_GET
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


@require_GET
def message_detail(request, message_id):
    message = get_object_or_404(Message, id=message_id)
    return JsonResponse({
        'id': message.id,
        'content': message.content,
        'chat': message.chat.id,
        'sender': message.sender.user.id,
        'created_at': message.created_at,
        'is_forwarded': message.is_forwarded,
    })


@require_POST
def create_message(request):
    message_content = request.POST.get('content')
    sender = ChatMember.objects.get(id=request.POST.get('sender'))
    message = Message.objects.create(content=message_content, sender=sender, chat=sender.chat)
    message.save()

    return JsonResponse({'new_message_id': message.id})


@require_http_methods(['PUT'])
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
            },
        })


@require_http_methods(['DELETE'])
def delete_message(request, message_id):
    message = get_object_or_404(Message, id=message_id)
    message.delete()
    return JsonResponse({'deleted_message_id': message_id})
