import sys
from datetime import datetime
from django_extensions.management.jobs import BaseJob
from django_asynctasks.models import AsyncTask
from django_asynctasks.locks import FileLock
from django.conf import settings


class Job(BaseJob):
    help = "Runs Async jobs."

    def execute(self):
        lock = FileLock('run_immediate_asyncjobs')

        if not lock.acquire():
            if settings.DEBUG: sys.stderr.write("Cannot acquire lock\n")
            return

        try:
            while True:
                next_task = AsyncTask.objects.filter(status='new', task_type='onetime', starts_at__lte=datetime.now())[:1]
                if not next_task: break

                try:
                    next_task = next_task[0]
                    next_task.execute()
                except:
                    sys.stderr.write("ERROR: Task \"%s\" failed (see admin logs for details)\n" % next_task.name)
        finally:
            lock.release()
