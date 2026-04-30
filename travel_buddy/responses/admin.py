from django.contrib import admin
from .models import Response

@admin.register(Response)
class ResponseAdmin(admin.ModelAdmin):
    list_display = ('id', 'route', 'user', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('route__title', 'user__username')
    actions = ['accept_responses', 'reject_responses']
    
    def accept_responses(self, request, queryset):
        updated = queryset.update(status='ACCEPTED')
        self.message_user(request, f'{updated} откликов принято.')
    accept_responses.short_description = 'Принять выбранные отклики'
    
    def reject_responses(self, request, queryset):
        updated = queryset.update(status='REJECTED')
        self.message_user(request, f'{updated} откликов отклонено.')
    reject_responses.short_description = 'Отклонить выбранные отклики'