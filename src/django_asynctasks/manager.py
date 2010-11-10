#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django_asynctasks.models import AsyncTask
from django_asynctasks.tasks import Task

class AsyncManager(object):
    @classmethod
    def get_tasks(bucket=None, schedule=None, status=None):
        rs = AsyncTask.objects.get_query_set()
        if bucket:
            rs = rs.filter(bucket=bucket)
        if schedule:
            rs = rs.filter(task_type=schedule)
        if status:
            rs = rs.filter(status=status)            
        return [ t for t in rs.all() ]

    @classmethod
    def get_defined_task_functions(self):
        import sys, imp
        from django.conf import settings

        for app in settings.INSTALLED_APPS:
            for name in [app, app + ".tasks"]:
                try:
                    tasks = __import__(app)
                except:
                    continue
                else:
                    if hasattr(tasks, 'tasks'):
                        tasks = tasks.tasks

                for obj in tasks.__dict__.values():
                    if isinstance(obj, Task):
                        import ipdb; ipdb.set_trace()
                    
        

