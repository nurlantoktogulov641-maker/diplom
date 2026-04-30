from django.urls import path
from . import views

urlpatterns = [
    path('room/<int:route_id>/', views.chat_room, name='chat_room'),
    path('private/<int:user_id>/', views.private_chat, name='private_chat'),
    path('unread-count/', views.unread_count, name='unread_count'),
    path('mark-read/<int:user_id>/', views.mark_as_read, name='mark_read'),
    path('list/', views.chat_list, name='chat_list'),



]