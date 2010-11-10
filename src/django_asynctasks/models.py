#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json, sys, traceback
from django.db import models
from datetime import datetime
from django_asynctasks.utils import import_namespace
from django_asynctasks.locks import FileLock
from django.core.mail import mail_admins
from django.conf import settings

TASK_TYPES = (
    ('onetime', 'One Time'),
    ('minutely', 'Minutely'),
    ('hourly', 'Hourly'),
    ('daily', 'Daily'),
)
TASK_STATUSES = (
    ('new', 'New'),
    ('running', 'Running'),
    ('done', 'Done'),
    ('failed', 'Failed'),
)

class AsyncTask(models.Model):
    name       = models.CharField(max_length=100)
    task_type  = models.CharField(max_length=10, choices=TASK_TYPES, default='onetime', verbose_name='Schedule')
    bucket     = models.CharField(max_length=50, default='__default__')

    function     = models.CharField(max_length=200)
    args         = models.TextField()
    kwargs       = models.TextField()
    return_value = models.TextField(blank=True, null=True)

    status     = models.CharField(max_length=10, default='new', choices=TASK_STATUSES)
    starts_at  = models.DateTimeField()

    created_at = models.DateTimeField(auto_now_add=True)
    started_at = models.DateTimeField(blank=True, null=True)
    ended_at   = models.DateTimeField(blank=True, null=True)

    class Meta:
        app_label = "Async Queue"
        verbose_name = "Task"

    @property
    def is_successful(self):
        if self.status not in ['done', 'failed']: return None
        return self.status == 'done'

    @property
    def duration(self):
        if not self.started_at or not self.ended_at:
            return None
        return self.ended_at - self.started_at

    def get_args(self):
        return json.loads(self.args or [])

    def get_kwargs(self):
        return json.loads(self.kwargs or {})

    def get_function(self):
        if self.function:
            return import_namespace(self.function)
        else:
            def empty(*args, **kwargs):
                pass
            return empty

    def get_return(self):
        if self.return_value:
            return json.loads(self.return_value)
        return None

    @classmethod
    def schedule(self, function_namespace, args, kwargs, when='hourly', label=None, bucket=None):
        task = AsyncTask()

        task.name = label or function_namespace
        if isinstance(when, datetime):
            task.task_type = 'onetime'
            task.starts_at = when            
        else:
            task.task_type = when
            task.starts_at = datetime.now()

        task.function   = function_namespace
        task.args       = json.dumps(args or [])
        task.kwargs     = json.dumps(kwargs or {})

        if bucket: task.bucket = bucket

        task.save()
        return task


    def execute(self):
        lock_name = (self.name or '') + '-' + str(self.pk)
        lock = FileLock(lock_name)

        if not lock.acquire(): return False

        try:
            self.status = 'running'
            self.started_at = datetime.now()
            self.save()

            args     = self.get_args()
            kwargs   = self.get_kwargs()
            function = self.get_function()
            ret      = None

            ret = function.run(*args, **kwargs)

            self.return_value = json.dumps(ret)
            self.status   = 'done'
            self.ended_at = datetime.now()
            self.save()

            return ret
        except:
            error = formatExceptionInfo() or '<unknown>'
            if hasattr(settings, 'ASYNCTASKS_MAIL_ON_ERROR') and settings.ASYNCTASKS_MAIL_ON_ERROR:
                mail_admins(subject='ERROR: ' + self.name, message=error, fail_silently=True)

            AsyncTaskError(task=self, error=error).save()

            self.status = 'failed'
            self.save()
            raise
        finally:
            lock.release()

    def __unicode__(self):
        return self.name


class AsyncTaskError(models.Model):
    task       = models.ForeignKey(AsyncTask, related_name='errors')
    error      = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = "Async Queue"
        verbose_name = "Error"

    def __unicode__(self):
        return self.task.name


def formatExceptionInfo(level = 6):
    error_type, error_value, trbk = sys.exc_info()
    tb_list = traceback.format_tb(trbk, level)    
    s = "Error: %s \nDescription: %s \nTraceback:" % (error_type.__name__, error_value)
    for i in tb_list:
        s += "\n" + i
    return s
