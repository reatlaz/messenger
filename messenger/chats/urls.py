from django.urls import path
from chats.views import chat_detail, chat_list, create_chat

urlpatterns = [
    path('', chat_list, name='chat_list'),
    path('<int:chat_id>/', chat_detail, name='chat_detail'),
    path('create/', create_chat, name='create_chat'),
]
