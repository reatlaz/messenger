from django.urls import path
from chats.views import ChatViewSet, MessageViewSet
from chats.views import add_member_to_chat, delete_member_from_chat
from users.views import user_detail
urlpatterns = [
    #path('user/<int:user_id>/list/', chat_list, name='chat_list'),
    path('<int:chat_id>/', ChatViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'delete': 'destroy'
    }), name='chat_page'),



    # спросить про REST URL для messages
    #path('<int:chat_id>/messages/list/', message_list, name='message_list'),

    path('<int:chat_id>/messages/', MessageViewSet.as_view({'get': 'list'}), name='message_page'),

    path('messages/<int:message_id>/', MessageViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'delete': 'destroy'
    }), name='message_page'),

    # path('messages/create/<int:chat_id>/', create_message, name='create_message'),
    # path('messages/edit/<int:message_id>/', edit_message, name='edit_message'),
    # path('messages/delete/<int:message_id>/', delete_message, name='delete_message'),

    path('<int:chat_id>/user/<int:user_id>/add/', add_member_to_chat, name='add_member_to_chat'),
    path('<int:chat_id>/user/<int:user_id>/delete/', delete_member_from_chat, name='delete_member_from_chat'),
]
