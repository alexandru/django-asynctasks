#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime
from functools import wraps
from inspect import getargspec
from django_asynctasks.models import AsyncTask

def task(label, when=None):
    if not when: 
        when = datetime.now()

    def wrap(f):
        @wraps(f)
        def delay(self, *args, **kwargs):
            namespace = f.__module__ + "." + f.__name__
            return AsyncTask.schedule(namespace, args=args, kwargs=kwargs, when=when, label=label)
        delay.argspec = getargspec(f)

        @wraps(f)
        def run(self, *args, **kwargs):
            return f(*args, **kwargs)
        run.argspec = getargspec(f)

        cls_dict = dict(run=run, delay=delay, __module__=f.__module__, when=when, label=label)
        return type(f.__name__, (Task,), cls_dict)()
    return wrap

class Task(object):    
    def run(self, *args, **kwargs):
        pass
    def delay(self, *args, **kwargs):
        pass
    def __call__(self, *args, **kwargs):
        return self.run(*args, **kwargs)
