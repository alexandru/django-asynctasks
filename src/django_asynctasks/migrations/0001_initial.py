# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'AsyncTask'
        db.create_table('django_asynctasks_asynctask', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('task_type', self.gf('django.db.models.fields.CharField')(default='onetime', max_length=10)),
            ('function', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('args', self.gf('django.db.models.fields.TextField')()),
            ('kwargs', self.gf('django.db.models.fields.TextField')()),
            ('return_value', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('status', self.gf('django.db.models.fields.CharField')(default='new', max_length=10)),
            ('starts_at', self.gf('django.db.models.fields.DateTimeField')()),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('started_at', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
        ))
        db.send_create_signal('django_asynctasks', ['AsyncTask'])

        # Adding model 'AsyncTaskError'
        db.create_table('django_asynctasks_asynctaskerror', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('task', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['django_asynctasks.AsyncTask'])),
            ('error', self.gf('django.db.models.fields.TextField')()),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('django_asynctasks', ['AsyncTaskError'])


    def backwards(self, orm):
        
        # Deleting model 'AsyncTask'
        db.delete_table('django_asynctasks_asynctask')

        # Deleting model 'AsyncTaskError'
        db.delete_table('django_asynctasks_asynctaskerror')


    models = {
        'django_asynctasks.asynctask': {
            'Meta': {'object_name': 'AsyncTask'},
            'args': ('django.db.models.fields.TextField', [], {}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'function': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'kwargs': ('django.db.models.fields.TextField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
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
            'task': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['django_asynctasks.AsyncTask']"})
        }
    }

    complete_apps = ['django_asynctasks']
