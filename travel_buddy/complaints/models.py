from django.db import models
from users.models import User

class Complaint(models.Model):
    REASONS = [
        ('spam', 'Спам'),
        ('offensive', 'Оскорбительное поведение'),
        ('fraud', 'Мошенничество'),
        ('fake', 'Фейковый аккаунт'),
        ('other', 'Другое'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'На рассмотрении'),
        ('approved', 'Подтверждена'),
        ('rejected', 'Отклонена'),
    ]
    
    complainant = models.ForeignKey(User, on_delete=models.CASCADE, related_name='complaints_made', verbose_name='Жалобщик')
    target_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='complaints_received', verbose_name='На кого жалоба')
    reason = models.CharField(max_length=20, choices=REASONS, verbose_name='Причина')
    description = models.TextField(verbose_name='Описание')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name='Статус')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата жалобы')
    
    class Meta:
        verbose_name = 'Жалоба'
        verbose_name_plural = 'Жалобы'
    
    def __str__(self):
        return f'{self.complainant.username} -> {self.target_user.username} ({self.reason})'