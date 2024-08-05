from django.contrib import admin
from .models import *
from django.contrib.auth import get_user_model

User = get_user_model()

# Register your models here.
admin.site.register(User)
admin.site.register(Role)
admin.site.register(Permission)
admin.site.register(OTP)