from django.urls import path
from chats.views import chat_list

urlpatterns = [
    path('', chat_list, name='chat_list')
]