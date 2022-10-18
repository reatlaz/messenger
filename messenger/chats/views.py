from django.http import JsonResponse
from django.shortcuts import render

def chat_list(request):
    return JsonResponse({'chats': []})

def chat_category(request, pk):
    return JsonResponse({'chat_pk': pk})