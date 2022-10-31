from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_GET, require_POST

@require_GET
def index(request):
    return JsonResponse({'chats': []})

@require_GET
def chat_list(request):
    return JsonResponse({'chats': ['Study group chat', 'Mom', 'VK HR']})

@require_GET
def chat_detail(request, chat_id):
    return  JsonResponse({'chat info': 'Beseda klassa'})

@require_POST
def create_chat(request):
    return  JsonResponse({'chat created': 'New chat'})


