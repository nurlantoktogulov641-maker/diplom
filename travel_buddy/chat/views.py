from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import models
from .models import Message, PrivateMessage
from routes.models import Route
from responses.models import Response
from travel_buddy.utils import log_action
from django.http import JsonResponse
from .models import PrivateMessage

@login_required
@log_action('Отправка сообщения в чат')
def chat_room(request, route_id):
    route = get_object_or_404(Route, id=route_id)
    
    is_participant = (request.user == route.author)
    if not is_participant:
        response = Response.objects.filter(route=route, user=request.user, status='ACCEPTED').first()
        if response:
            is_participant = True
    
    if not is_participant:
        messages.warning(request, 'У вас нет доступа к этому чату')
        return redirect('route_detail', route_id=route.id)
    
    if request.method == 'POST':
        text = request.POST.get('text')
        if text:
            Message.objects.create(
                route=route,
                sender=request.user,
                text=text
            )
        return redirect('chat_room', route_id=route.id)
    
    messages_list = Message.objects.filter(route=route).order_by('created_at')
    
    return render(request, 'chat/room.html', {
        'route': route,
        'messages': messages_list
    })


@login_required
def private_chat(request, user_id):
    """Личный чат с пользователем"""
    from users.models import User
    receiver = get_object_or_404(User, id=user_id)
    
    if request.user == receiver:
        messages.warning(request, 'Нельзя написать самому себе')
        return redirect('profile', user_id=user_id)
    
    # Переименовали messages_list (чтобы не конфликтовать с django.contrib.messages)
    messages_list = PrivateMessage.objects.filter(
        (models.Q(sender=request.user, receiver=receiver) |
         models.Q(sender=receiver, receiver=request.user))
    ).order_by('created_at')
    
    messages_list.filter(receiver=request.user, is_read=False).update(is_read=True)
    
    if request.method == 'POST':
        text = request.POST.get('text')
        if text:
            PrivateMessage.objects.create(
                sender=request.user,
                receiver=receiver,
                text=text
            )
            messages.success(request, 'Сообщение отправлено!')
            return redirect('private_chat', user_id=user_id)
    
    return render(request, 'chat/private_chat.html', {
        'receiver': receiver,
        'messages': messages_list
    })
@login_required
def unread_count(request):
    """Возвращает количество непрочитанных личных сообщений"""
    count = PrivateMessage.objects.filter(receiver=request.user, is_read=False).count()
    return JsonResponse({'count': count})
@login_required
def mark_as_read(request, user_id):
    """Отмечает все сообщения от пользователя как прочитанные"""
    from users.models import User
    sender = get_object_or_404(User, id=user_id)
    PrivateMessage.objects.filter(sender=sender, receiver=request.user, is_read=False).update(is_read=True)
    return JsonResponse({'status': 'ok'})
@login_required
def chat_list(request):
    """Список всех чатов пользователя"""
    from django.db.models import Max
    
    # Находим всех пользователей, с которыми были сообщения
    sent_users = PrivateMessage.objects.filter(sender=request.user).values_list('receiver_id', flat=True)
    received_users = PrivateMessage.objects.filter(receiver=request.user).values_list('sender_id', flat=True)
    chat_user_ids = set(list(sent_users) + list(received_users))
    
    chats = []
    from users.models import User
    for user_id in chat_user_ids:
        other_user = User.objects.get(id=user_id)
        
        # Получаем последнее сообщение
        last_message = PrivateMessage.objects.filter(
            (models.Q(sender=request.user, receiver=other_user) |
             models.Q(sender=other_user, receiver=request.user))
        ).order_by('-created_at').first()
        
        # Считаем непрочитанные сообщения от этого пользователя
        unread_count = PrivateMessage.objects.filter(
            sender=other_user, receiver=request.user, is_read=False
        ).count()
        
        chats.append({
            'user': other_user,
            'last_message': last_message.text[:50] if last_message else '',
            'unread_count': unread_count,
        })
    
    # Сортируем по времени последнего сообщения
    chats.sort(key=lambda x: x.get('last_message', ''), reverse=True)
    
    return render(request, 'chat/chat_list.html', {'chats': chats})