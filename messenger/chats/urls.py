from django.urls import path
from chats.views import chat_list, chat_detail, create_chat, delete_chat, edit_chat
from chats.views import message_list, message_detail, create_message, edit_message, delete_message

urlpatterns = [
    path('list/<int:user_id>/', chat_list, name='chat_list'),
    path('<int:chat_id>/', chat_detail, name='chat_detail'),
    path('create/', create_chat, name='create_chat'),
    path('edit/<int:chat_id>/', edit_chat, name='edit_chat'),
    path('delete/<int:chat_id>/', delete_chat, name='delete_chat'),

    # спросить про REST URL для messages
    # лучше одно поле DateTimeField или два DateField + TimeField?
    path('<int:chat_id>/messages/list/', message_list, name='message_detail'),
    path('messages/<int:message_id>/', message_detail, name='message_detail'),
    path('messages/create/', create_message, name='create_message'),
    path('messages/edit/<int:message_id>/', edit_message, name='edit_message'),
    path('messages/delete/<int:message_id>/', delete_message, name='delete_message'),
]
