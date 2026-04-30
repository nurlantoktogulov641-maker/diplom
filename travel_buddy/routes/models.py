from django.db import models
from users.models import User

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name='Название')
    slug = models.CharField(max_length=50, unique=True, blank=True, verbose_name='Slug')

    def save(self, *args, **kwargs):
        if not self.slug:
            from django.utils.text import slugify
            self.slug = slugify(self.name, allow_unicode=True)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'


class Route(models.Model):
    STATUS_CHOICES = [
        ('ACTIVE', 'Активен'),
        ('ARCHIVED', 'Архив'),
        ('CANCELLED', 'Отменён'),
    ]

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='routes', verbose_name='Автор')
    title = models.CharField(max_length=200, verbose_name='Название')
    description = models.TextField(blank=True, verbose_name='Описание')
    countries = models.CharField(max_length=255, verbose_name='Страны')
    cities = models.CharField(max_length=255, blank=True, verbose_name='Города')
    start_date = models.DateField(verbose_name='Дата начала')
    end_date = models.DateField(verbose_name='Дата окончания')
    budget = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name='Бюджет')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ACTIVE', verbose_name='Статус')
    views_count = models.PositiveIntegerField(default=0, verbose_name='Просмотры')
    image = models.ImageField(upload_to='routes/', blank=True, null=True, verbose_name='Изображение')
    places = models.JSONField(default=list, blank=True, verbose_name='Места посещения')
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True, verbose_name='Широта')
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True, verbose_name='Долгота')
    location = models.CharField(max_length=500, blank=True, verbose_name='Ссылка на карту')
    
    # Поля для маршрута
    start_city = models.CharField(max_length=200, blank=True, verbose_name='Город отправления')
    end_city = models.CharField(max_length=200, blank=True, verbose_name='Город назначения')
    waypoints = models.CharField(max_length=500, blank=True, verbose_name='Промежуточные точки')
    city = models.CharField(max_length=200, blank=True, verbose_name='Город для карты')
    
    tags = models.ManyToManyField(Tag, blank=True, related_name='routes', verbose_name='Теги')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Маршрут'
        verbose_name_plural = 'Маршруты'


class RouteImage(models.Model):
    route = models.ForeignKey(Route, on_delete=models.CASCADE, related_name='extra_images', verbose_name='Маршрут')
    image = models.ImageField(upload_to='routes/', verbose_name='Изображение')
    order = models.PositiveIntegerField(default=0, verbose_name='Порядок')

    class Meta:
        ordering = ['order']
        verbose_name = 'Изображение маршрута'
        verbose_name_plural = 'Изображения маршрутов'

    def __str__(self):
        return f"Изображение для {self.route.title}"


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites', verbose_name='Пользователь')
    route = models.ForeignKey(Route, on_delete=models.CASCADE, related_name='favorited_by', verbose_name='Маршрут')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')

    class Meta:
        unique_together = ('user', 'route')
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'

    def __str__(self):
        return f"{self.user.username} -> {self.route.title}"
class RouteComment(models.Model):
    route = models.ForeignKey(Route, on_delete=models.CASCADE, related_name='comments', verbose_name='Маршрут')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='route_comments', verbose_name='Автор')
    text = models.TextField(verbose_name='Текст комментария')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Комментарий к маршруту'
        verbose_name_plural = 'Комментарии к маршрутам'
    
    def __str__(self):
        return f'{self.author.username}: {self.text[:50]}'
class RouteComment(models.Model):
    route = models.ForeignKey(Route, on_delete=models.CASCADE, related_name='comments', verbose_name='Маршрут')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='route_comments', verbose_name='Автор')
    text = models.TextField(verbose_name='Текст комментария')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Комментарий к маршруту'
        verbose_name_plural = 'Комментарии к маршрутам'
    
    def __str__(self):
        return f'{self.author.username}: {self.text[:50]}'


class RouteLike(models.Model):
    route = models.ForeignKey(Route, on_delete=models.CASCADE, related_name='likes', verbose_name='Маршрут')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='route_likes', verbose_name='Пользователь')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата')

    class Meta:
        unique_together = ('route', 'user')
        verbose_name = 'Лайк маршрута'
        verbose_name_plural = 'Лайки маршрутов'

    def __str__(self):
        return f'{self.user.username} лайкнул {self.route.title}'