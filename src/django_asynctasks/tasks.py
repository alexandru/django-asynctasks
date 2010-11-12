#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime
from functools import wraps
from inspect import getargspec
from django_asynctasks.models import AsyncTask

HIGH=1
NORMAL=2
LOW=3

def define(label, schedule=None, bucket=None, priority=2):
    if not schedule: 
        schedule = 'onetime'
    if not bucket:
        bucket = '__default__'

    def wrap(f):
        function_namespace = f.__module__ + "." + f.__name__

        @wraps(f)
        def delay(self, *args, **kwargs):
            try:
                override_priority = kwargs.pop('priority') or 2
            except KeyError:
                override_priority = priority

            try:
                override_bucket = kwargs.pop('bucket') or None
            except KeyError:
                override_bucket = bucket

            return AsyncTask.schedule(function_namespace, args=args, kwargs=kwargs, 
                                      when='onetime', label=label, 
                                      bucket=override_bucket, 
                                      priority=override_priority)
        delay.argspec = getargspec(f)

        @wraps(f)
        def run(self, *args, **kwargs):
            return f(*args, **kwargs)
        run.argspec = getargspec(f)

        cls_dict = dict(run=run, delay=delay, __module__=f.__module__, schedule=schedule, label=label)
        return type(f.__name__, (Task,), cls_dict)()
    return wrap


class Task(object):    
    def run(self, *args, **kwargs):
        pass
    def delay(self, *args, **kwargs):
        pass
    def __call__(self, *args, **kwargs):
        return self.run(*args, **kwargs)
