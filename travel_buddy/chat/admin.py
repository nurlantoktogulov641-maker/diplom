from django.contrib import admin
from .models import Message
from .models import PrivateMessage

admin.site.register(Message)
admin.site.register(PrivateMessage)
