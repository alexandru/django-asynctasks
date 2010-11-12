# encoding: utf-8
import datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models

class Migration(DataMigration):

    def forwards(self, orm):
        db.execute("CREATE INDEX asynctasks_new ON django_asynctasks_asynctask (status, task_type, bucket, priority, id)")


    def backwards(self, orm):
        db.execute("DROP INDEX asynctasks_new ON django_asynctasks_asynctask")


    models = {
        'django_asynctasks.asynctask': {
            'Meta': {'object_name': 'AsyncTask'},
            'args': ('django.db.models.fields.TextField', [], {}),
            'bucket': ('django.db.models.fields.CharField', [], {'default': "'__default__'", 'max_length': '50'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'ended_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'function': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'kwargs': ('django.db.models.fields.TextField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'priority': ('django.db.models.fields.IntegerField', [], {'default': '2', 'max_length': '10'}),
            'return_value': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'started_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'starts_at': ('django.db.models.fields.DateTimeField', [], {}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'new'", 'max_length': '10'}),
            'task_type': ('django.db.models.fields.CharField', [], {'default': "'onetime'", 'max_length': '10'})
        },
        'django_asynctasks.asynctaskerror': {
            'Meta': {'object_name': 'AsyncTaskError'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'error': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'task': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'errors'", 'to': "orm['django_asynctasks.AsyncTask']"})
        }
    }

    complete_apps = ['django_asynctasks']
