import logging
import functools
from django.utils.timezone import now

logger = logging.getLogger('travel_buddy')

def log_action(message):
    """Декоратор для логирования действий пользователя"""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(request, *args, **kwargs):
            if request.user.is_authenticated:
                log_msg = f"[{now()}] Пользователь: {request.user.username} | IP: {request.META.get('REMOTE_ADDR')} | {message} | URL: {request.path}"
            else:
                log_msg = f"[{now()}] Пользователь: Аноним | IP: {request.META.get('REMOTE_ADDR')} | {message} | URL: {request.path}"
            logger.info(log_msg)
            return func(request, *args, **kwargs)
        return wrapper
    return decorator
from django.core.mail import send_mail
from django.conf import settings

def send_notification(email, subject, message):
    """Отправка email уведомления"""
    try:
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [email],
            fail_silently=False,
        )
    except Exception as e:
        print(f"Ошибка отправки email: {e}")