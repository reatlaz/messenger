from django.urls import path
from chats.views import ChatViewSet, MessageViewSet, MemberViewSet
urlpatterns = [
    path('user/<int:user_id>/', ChatViewSet.as_view({
        'get': 'list'
    }), name='chat_list'),

    path('<int:chat_id>/', ChatViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'delete': 'destroy'
    }), name='chat_page'),

    path('create/', ChatViewSet.as_view({
        'post': 'create',
    }), name='chat_page'),


    path('<int:chat_id>/messages/', MessageViewSet.as_view({
        'get': 'list',
        'post': 'create',
    }), name='message_list'),

    path('messages/<int:message_id>/', MessageViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'delete': 'destroy'
    }), name='message_page'),

    path('messages/<int:message_id>/mark_as_read/', MessageViewSet.as_view({
        'put': 'partial_update',
    }), name='mark_message_as_read'),


    path('<int:chat_id>/user/<int:user_id>/add_remove/', MemberViewSet.as_view({
        'put': 'create',
        'delete': 'destroy'
    }), name='add_remove_chat_member'),

]
