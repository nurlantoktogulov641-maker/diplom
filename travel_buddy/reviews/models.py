from django.db import models
from users.models import User
from routes.models import Route
from django.core.validators import MinValueValidator, MaxValueValidator

class Review(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews_written', verbose_name='Автор')
    target_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews_received', verbose_name='Получатель')
    route = models.ForeignKey(Route, on_delete=models.CASCADE, related_name='reviews', verbose_name='Маршрут')
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], verbose_name='Оценка (1-5)')
    comment = models.TextField(blank=True, verbose_name='Комментарий')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    class Meta:
        unique_together = ('author', 'target_user', 'route')
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    def __str__(self):
        return f'{self.author.username} → {self.target_user.username}: {self.rating}'