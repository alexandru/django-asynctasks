import sys
from datetime import datetime
from django_extensions.management.jobs import BaseJob
from django_asynctasks.models import AsyncTask
from django_asynctasks.locks import AcquireLock
from django.conf import settings


class Job(BaseJob):
    help = "Runs Async jobs."

    def execute(self):
        buckets_rs = AsyncTask.objects.filter(status='new', task_type='onetime')\
            .order_by('priority').values('bucket').distinct()
        buckets    = []

        for bucket in buckets_rs:
            if not bucket['bucket'] in buckets:
                buckets.append(bucket['bucket'])

        for bucket in buckets:
            with AcquireLock(bucket) as has_lock:
                if not has_lock: continue

                while True:
                    rs = AsyncTask.objects.filter(bucket=bucket, status='new',  task_type='onetime', 
                                                  starts_at__lte=datetime.now()).order_by('priority', 'id')

                    next_task = rs.all()[:1]
                    if not next_task: break

                    try:
                        next_task = next_task[0]
                        print next_task.name
                        next_task.execute()
                    except:
                        sys.stderr.write("ERROR: Task \"%s\" failed (see admin logs for details)\n" % next_task.name)
