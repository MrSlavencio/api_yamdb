from django.contrib import admin
# django.contrib.auth.admin.UserAdmin

from .models import User

admin.site.register(User)
