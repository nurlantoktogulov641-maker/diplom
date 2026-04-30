from django.urls import path
from . import views
from django.urls import path, include

urlpatterns = [
    path('register/', views.register, name='register'),
    path('profile/<int:user_id>/', views.profile, name='profile'),
    path('profile/<int:user_id>/edit/', views.profile_edit, name='profile_edit'),
    path('my-routes/', views.my_routes, name='my_routes'),
    path('my-responses/', views.my_responses, name='my_responses'),
    path('captcha/', include('captcha.urls')),
]