from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Count, Q, Avg
from django.utils import timezone
from datetime import datetime, timedelta
from routes.models import Route
from users.models import User
from responses.models import Response
from reviews.models import Review
from django.db import models

@staff_member_required
def admin_dashboard(request):
    # Статистика
    total_users = User.objects.filter(is_active=True).count()
    total_routes = Route.objects.count()
    active_routes = Route.objects.filter(status='ACTIVE').count()
    total_responses = Response.objects.count()
    total_reviews = Review.objects.count()
    avg_rating = Review.objects.aggregate(avg=models.Avg('rating'))['avg'] or 0
    
    # Регистрации по дням (последние 30 дней)
    today = timezone.now().date()
    start_date = today - timedelta(days=30)
    
    registrations_by_day = User.objects.filter(
        date_joined__date__gte=start_date
    ).extra({'day': "date(date_joined)"}).values('day').annotate(
        count=Count('id')
    ).order_by('day')
    
    routes_by_day = Route.objects.filter(
        created_at__date__gte=start_date
    ).extra({'day': "date(created_at)"}).values('day').annotate(
        count=Count('id')
    ).order_by('day')
    
    # Подготовка данных для графика (с преобразованием строки в дату)
    reg_days = []
    reg_counts = []
    for r in registrations_by_day:
        day_val = r['day']
        if isinstance(day_val, str):
            day_obj = datetime.strptime(day_val, '%Y-%m-%d').date()
        else:
            day_obj = day_val
        reg_days.append(day_obj.strftime('%d.%m'))
        reg_counts.append(r['count'])
    
    route_days = []
    route_counts = []
    for r in routes_by_day:
        day_val = r['day']
        if isinstance(day_val, str):
            day_obj = datetime.strptime(day_val, '%Y-%m-%d').date()
        else:
            day_obj = day_val
        route_days.append(day_obj.strftime('%d.%m'))
        route_counts.append(r['count'])
    
    # Популярные маршруты
    popular_routes = Route.objects.annotate(
        response_count=Count('responses')
    ).order_by('-response_count', '-views_count')[:5]
    
    # Активные пользователи (по откликам)
    active_users = User.objects.annotate(
        response_count=Count('responses')
    ).filter(response_count__gt=0).order_by('-response_count')[:5]
    
    context = {
        'total_users': total_users,
        'total_routes': total_routes,
        'active_routes': active_routes,
        'total_responses': total_responses,
        'total_reviews': total_reviews,
        'avg_rating': round(avg_rating, 2),
        'reg_days': reg_days,
        'reg_counts': reg_counts,
        'route_days': route_days,
        'route_counts': route_counts,
        'popular_routes': popular_routes,
        'active_users': active_users,
    }
    
    return render(request, 'admin/dashboard.html', context)