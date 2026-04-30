from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.views import LoginView, LogoutView

class NoCSRFLoginView(LoginView):
    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('routes.urls')),
    path('users/', include('users.urls')),
    path('responses/', include('responses.urls')),
    path('reviews/', include('reviews.urls')),
    path('chat/', include('chat.urls')),
    path('login/', NoCSRFLoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('complaints/', include('complaints.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)