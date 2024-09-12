from typing import Any
from django.contrib import admin
from .models import User
from django.contrib.auth.hashers import make_password


# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'email', 'role']
    readonly_fields = ('created_at', 'updated_at')
    search_fields = ('username', 'email')
    list_filter = ('role',)

    def save_model(self, request: Any, obj: Any, form: Any, change: Any):
        '''
        save hash password when create new user from django admin panel
        '''
        if obj.is_new:
            obj.password = make_password(obj.password)
        return super().save_model(request, obj, form, change)



admin.site.register(User, UserAdmin)

