
from south.db import db
from django.db import models
from banquise.web.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'MetaBug'
        db.create_table('web_metabug', (
            ('id', orm['web.metabug:id']),
            ('bugid', orm['web.metabug:bugid']),
            ('href', orm['web.metabug:href']),
            ('type', orm['web.metabug:type']),
            ('title', orm['web.metabug:title']),
            ('metainfo', orm['web.metabug:metainfo']),
        ))
        db.send_create_signal('web', ['MetaBug'])
        
        # Adding field 'MetaInfo.status'
        db.add_column('web_metainfo', 'status', orm['web.metainfo:status'])
        
        # Adding field 'MetaInfo.description'
        db.add_column('web_metainfo', 'description', orm['web.metainfo:description'])
        
        # Deleting field 'MetaInfo.title'
        db.delete_column('web_metainfo', 'title')
        
        # Deleting field 'MetaInfo.href'
        db.delete_column('web_metainfo', 'href')
        
    
    
    def backwards(self, orm):
        
        # Deleting model 'MetaBug'
        db.delete_table('web_metabug')
        
        # Deleting field 'MetaInfo.status'
        db.delete_column('web_metainfo', 'status')
        
        # Deleting field 'MetaInfo.description'
        db.delete_column('web_metainfo', 'description')
        
        # Adding field 'MetaInfo.title'
        db.add_column('web_metainfo', 'title', orm['web.metainfo:title'])
        
        # Adding field 'MetaInfo.href'
        db.add_column('web_metainfo', 'href', orm['web.metainfo:href'])
        
    
    
    models = {
        'web.contract': {
            'customer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['web.Customer']"}),
            'end_date': ('django.db.models.fields.DateField', [], {}),
            'hosts': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['web.Host']", 'symmetrical': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'license': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'start_date': ('django.db.models.fields.DateField', [], {})
        },
        'web.customer': {
            'contact': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'email': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '150'})
        },
        'web.host': {
            'hash': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'public_ip': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'release': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'web.metabug': {
            'bugid': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'href': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'metainfo': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['web.MetaInfo']", 'null': 'True'}),
            'title': ('django.db.models.fields.TextField', [], {}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        'web.metainfo': {
            'description': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'updateid': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'web.package': {
            'Meta': {'unique_together': "(('name', 'arch', 'version', 'release'),)"},
            'arch': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'metainfo': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['web.MetaInfo']", 'null': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'release': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'repo': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '15', 'blank': 'True'}),
            'version': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'web.serverpackages': {
            'date_available': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'date_installed': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'date_synced': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'host': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['web.Host']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'new_install': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'package': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['web.Package']"}),
            'package_installed': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'package_skipped': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'removed': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'to_install': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'})
        }
    }
    
    complete_apps = ['web']
