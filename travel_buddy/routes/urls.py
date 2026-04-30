from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('route/<int:route_id>/', views.route_detail, name='route_detail'),
    path('route/create/', views.route_create, name='route_create'),
    path('route/<int:route_id>/edit/', views.route_edit, name='route_edit'),
    path('route/<int:route_id>/delete/', views.route_delete, name='route_delete'),
    
    # Избранное
    path('favorites/add/<int:route_id>/', views.add_to_favorites, name='add_to_favorites'),
    path('favorites/remove/<int:route_id>/', views.remove_from_favorites, name='remove_from_favorites'),
    path('favorites/', views.my_favorites, name='my_favorites'),
    path('route/<int:route_id>/participants/', views.route_participants, name='route_participants'),
    path('export/<int:route_id>/', views.export_route_pdf, name='export_route_pdf'),
    path('like/<int:route_id>/', views.toggle_like, name='toggle_like'),

]