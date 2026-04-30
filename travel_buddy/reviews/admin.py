from django.contrib import admin
from .models import Review

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'target_user', 'route', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('author__username', 'target_user__username', 'route__title')
    actions = ['delete_selected']  # стандартное удаление уже есть