from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_GET, require_POST


@require_GET 
def index(request):
    return render(request, 'chats/index.html')


@require_GET
def chat_list(request):
    return JsonResponse(
        {'chats': [
            {
                'id': 5,
                'name': 'Study group chat',
                'last_message': 'Скиньте дз плз',
                'last_message_time': '17:18',
            },
            {
                'id': 2,
                'name': 'Mom',
                'last_message': 'Шапку надень!',
                'last_message_time': '11:00',
            },
            {
                'id': 7,
                'name': 'VK HR',
                'last_message': 'Давайте назначим дату интервью',
                'last_message_time': '14:31',
            }
        ]})


@require_GET
def chat_detail(request, chat_id):
    return JsonResponse({
        'chat_info': {
            'id': chat_id,
            'description': 'This is the chat of our study group',
            'name': 'Group chat',
            'owner': 'reatlaz',
            'members': ['reatlaz', 'ivan', 'kirill'],
        },
        'messages': [
            {
                'id': 4543,
                'text': 'Всем привет!',
                'sender': 'reatlaz',
                'is_forwarded': False,
                'date': '30 October',
                'time': '14:10',

            },
            {
                'id': 3452534,
                'text': 'Привет!',
                'sender': 'ivan',
                'is_forwarded': False,
                'date': '01 November',
                'time': '17:20',
            }
        ]

    })


@require_POST
def create_chat(request):
    return JsonResponse({'new_chat_id': '14'})
