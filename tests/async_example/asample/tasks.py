import time
from django_asynctasks import tasks

@tasks.define(label='Normal in Bucket 1', bucket='tests', priority=tasks.NORMAL)
def bucket_1_normal(**kwargs):
    print kwargs['bucket']

@tasks.define(label='HIGH in Bucket 2', bucket='big-shit', priority=tasks.HIGH)
def bucket_2_high(**kwargs):
    priority = kwargs['priority']
    bucket   = kwargs['bucket']

    print kwargs['bucket']

    bucket_1_normal.delay(priority=priority, bucket=bucket)

@tasks.define(label='LOW in Bucket 2', bucket='big-shit', priority=tasks.LOW)
def bucket_2_low(**kwargs):
    time.sleep(200)


