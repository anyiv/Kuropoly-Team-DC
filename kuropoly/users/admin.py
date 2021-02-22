from django.contrib import admin
from users.models import UserType, User

# Register your models here.
admin.site.register(UserType)
admin.site.register(User)