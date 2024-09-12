from django.contrib import admin
from .models import Tool


class ToolAdmin(admin.ModelAdmin):
    list_display = ['name', 'active']
    readonly_fields = ('created_at', 'updated_at')
    search_fields = ('name',)
    list_filter = ('active',)


admin.site.register(Tool, ToolAdmin)
