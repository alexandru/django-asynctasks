from django.contrib import admin
from django_asynctasks.models import AsyncTask, AsyncTaskError

class AsyncTaskAdmin(admin.ModelAdmin):
    list_display   = ('name', 'function', 'bucket', 'task_type', 'formatted_status', 
                      'started_at', 'duration', 'created_at',)
    list_filter    = ('created_at', 'task_type', 'status')

    actions = None
    search_fields  = ('name', 'function')

    def formatted_status(self, task):
        if task.status in ['new', 'running']:
            return "<span style='color: blue'><b>" + task.status + "</b></span>"
        if task.status == 'done':
            return "<span style='color: green'><b>DONE</b></span>"
        if task.status in ['failed', 'stopped']:
            return "<span style='color: red'><b>%s</b></span>" % task.status.upper()

    formatted_status.allow_tags = True
    formatted_status.short_description = 'Status'


admin.site.register(AsyncTask, AsyncTaskAdmin)
admin.site.register(AsyncTaskError)
