from django.urls import path
from chats.views import chat_list, chat_detail, create_chat, delete_chat, edit_chat
from chats.views import message_list, message_detail, create_message, edit_message, delete_message
from chats.views import add_member_to_chat, delete_member_from_chat
from users.views import user_detail
urlpatterns = [
    path('user/<int:user_id>/list/', chat_list, name='chat_list'),
    path('<int:chat_id>/', chat_detail, name='chat_detail'),
    path('create/', create_chat, name='create_chat'),
    path('edit/<int:chat_id>/', edit_chat, name='edit_chat'),
    path('delete/<int:chat_id>/', delete_chat, name='delete_chat'),

    # спросить про REST URL для messages
    path('<int:chat_id>/messages/list/', message_list, name='message_detail'),
    path('messages/<int:message_id>/', message_detail, name='message_detail'),
    path('messages/create/<int:chat_id>/', create_message, name='create_message'),
    path('messages/edit/<int:message_id>/', edit_message, name='edit_message'),
    path('messages/delete/<int:message_id>/', delete_message, name='delete_message'),

    path('<int:chat_id>/user/<int:user_id>/add/', add_member_to_chat, name='add_member_to_chat'),
    path('<int:chat_id>/user/<int:user_id>/delete/', delete_member_from_chat, name='delete_member_from_chat'),
]
