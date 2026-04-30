from django.urls import path
from . import views

urlpatterns = [
    path('complain/<int:user_id>/', views.complain, name='complain'),
]