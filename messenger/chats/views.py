from django.http import JsonResponse, HttpResponse, HttpResponseRedirect, Http404
from django.utils.html import escape
from django.shortcuts import render
from django.views.decorators.http import require_GET, require_POST

from.models import Chat

@require_GET
def index(request):
    return HttpResponse('''<h1>Welcome to my messenger app!</h1>
    <ul>
        <li>Список чатов: <a href=../chats/list/>chats/list/</a></li>
        <li>Страница чата: <a href=../chats/?chat_id=1>chats/?chat_id=1</a></li>
        <li>Создание чата: Проверять в <b>Postman</b></li>
    </ul>''')



@require_GET
def chat_list(request):
    chats = Chat.objects.values()

    return JsonResponse({'chats': list(chats)})

@require_GET
def chat_detail(request):
    try:
        chat_id = request.GET.get('chat_id')
        chat = Chat.objects.get(id=chat_id)
    except Chat.DoesNotExist:
        raise Http404
    return HttpResponse(chat, content_type='text/plain')

@require_POST
def create_chat(request):

    chat_name = request.GET.get('chat_name')
    user_ids = request.GET.get('users[]').split(',')
    print(user_ids)
    chat = Chat.objects.create(name=chat_name)
    chat.users.set(user_ids)
    chat.save()
#    return HttpResponse('''<p>Chat id: ''' + escape(chat.id) + ''', chat name: ''' + escape(escape(chat_name)) + '''</p>''')
    return HttpResponseRedirect('http://localhost:8000/chats/')

