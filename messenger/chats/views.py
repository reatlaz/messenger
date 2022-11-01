from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_GET, require_POST

@require_GET
def index(request):
    return HttpResponse('''<h1>Welcome to my messenger app!</h1>
    <ul>
        <li>Список чатов: <a href=../chats>chats/</a></li>
        <li>Страница чата: <a href=../chats/1/>chats/1/</a></li>
        <li>Создание чата: Проверять в <b>Postman</b></li>
    </ul>''')

@require_GET
def chat_list(request):
    return JsonResponse({'chats': ['Study group chat', 'Mom', 'VK HR']})

@require_GET
def chat_detail(request, chat_id):
    return  JsonResponse({'chat info': 'Beseda klassa'})

@require_POST
def create_chat(request):
    return  JsonResponse({'chat created': 'New chat'})


