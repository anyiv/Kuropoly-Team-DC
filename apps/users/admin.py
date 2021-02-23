from django.contrib import admin
from apps.users.models import UserType, User

# Register your models here.
admin.site.register(UserType)
admin.site.register(User)