
from south.db import db
from django.db import models
from banquise.web.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding field 'MetaInfo.updateid'
        db.add_column('web_metainfo', 'updateid', orm['web.metainfo:updateid'])
        
        # Deleting field 'MetaInfo.update_id'
        db.delete_column('web_metainfo', 'update_id')
        
    
    
    def backwards(self, orm):
        
        # Deleting field 'MetaInfo.updateid'
        db.delete_column('web_metainfo', 'updateid')
        
        # Adding field 'MetaInfo.update_id'
        db.add_column('web_metainfo', 'update_id', orm['web.metainfo:update_id'])
        
    
    
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
        'web.metainfo': {
            'href': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.TextField', [], {}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'updateid': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'})
        },
        'web.package': {
            'Meta': {'unique_together': "(('name', 'arch', 'version', 'release'),)"},
            'arch': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'metainfo': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['web.MetaInfo']"}),
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