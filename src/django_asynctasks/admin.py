from django.contrib import admin
from django_asynctasks.models import AsyncTask, AsyncTaskError

class AsyncTaskAdmin(admin.ModelAdmin):
    list_display   = ('name', 'function', 'task_type', 'starts_at', 'status', 'started_at', 'created_at')
    list_filter    = ('created_at', 'task_type', 'status')

    actions = None
    search_fields  = ('name', 'function')

admin.site.register(AsyncTask, AsyncTaskAdmin)
admin.site.register(AsyncTaskError)
