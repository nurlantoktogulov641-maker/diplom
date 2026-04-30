from django.db import models
from users.models import User
from routes.models import Route

class Message(models.Model):
    route = models.ForeignKey(Route, on_delete=models.CASCADE, related_name='messages', verbose_name='Маршрут')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages', verbose_name='Отправитель')
    text = models.TextField(verbose_name='Текст')
    is_read = models.BooleanField(default=False, verbose_name='Прочитано')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата отправки')

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'

    def __str__(self):
        return f'{self.sender.username}: {self.text[:50]}'


class PrivateMessage(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_private_messages', verbose_name='Отправитель')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_private_messages', verbose_name='Получатель')
    text = models.TextField(verbose_name='Текст сообщения')
    is_read = models.BooleanField(default=False, verbose_name='Прочитано')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата отправки')

    class Meta:
        ordering = ['created_at']
        verbose_name = 'Личное сообщение'
        verbose_name_plural = 'Личные сообщения'

    def __str__(self):
        return f'От {self.sender.username} к {self.receiver.username}: {self.text[:50]}'