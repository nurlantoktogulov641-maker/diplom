from django.db import models
from users.models import User
from routes.models import Route

class Response(models.Model):
    STATUS_CHOICES = [('PENDING', 'Ожидание'), ('ACCEPTED', 'Принят'), ('REJECTED', 'Отклонён')]
    route = models.ForeignKey(Route, on_delete=models.CASCADE, related_name='responses', verbose_name='Маршрут')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='responses', verbose_name='Пользователь')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING', verbose_name='Статус')
    message = models.TextField(blank=True, verbose_name='Сообщение')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата отправки')

    class Meta:
        unique_together = ('route', 'user')
        verbose_name = 'Отклик'
        verbose_name_plural = 'Отклики'

    def __str__(self):
        return f'{self.user.username} -> {self.route.title}'