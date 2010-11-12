import time
from django_asynctasks import tasks

@tasks.define(label='Normal in Bucket 1', bucket='tests', priority=tasks.NORMAL)
def bucket_1_normal():
    pass

@tasks.define(label='HIGH in Bucket 2', bucket='big-shit', priority=tasks.HIGH)
def bucket_2_high():
    pass

@tasks.define(label='LOW in Bucket 2', bucket='big-shit', priority=tasks.LOW)
def bucket_2_low():
    time.sleep(200)

@tasks.define(label='task that throws exceptions', bucket='tests')
def throw_something(what):
    raise Exception(what)

@tasks.define(label='task that throws exceptions', bucket='tests', schedule='hourly')
def hourly_say_hi(what='Alex'):
    return "Hello " + what
