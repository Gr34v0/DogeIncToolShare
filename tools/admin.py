from django.contrib import admin
from tools.models import *

# Register your models here.

class ToolAdmin(admin.ModelAdmin):
    fields = ['owner', 'tool_type']
    
admin.site.register(Tool, ToolAdmin)
