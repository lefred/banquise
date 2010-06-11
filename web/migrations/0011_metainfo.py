
from south.db import db
from django.db import models
from banquise.web.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'MetaInfo'
        db.create_table('web_metainfo', (
            ('id', orm['web.metainfo:id']),
            ('update_id', orm['web.metainfo:update_id']),
            ('href', orm['web.metainfo:href']),
            ('type', orm['web.metainfo:type']),
            ('title', orm['web.metainfo:title']),
        ))
        db.send_create_signal('web', ['MetaInfo'])
        
        # Adding field 'Package.metainfo'
        db.add_column('web_package', 'metainfo', orm['web.package:metainfo'])
        
        # Deleting field 'Package.update_id'
        db.delete_column('web_package', 'update_id')
        
    
    
    def backwards(self, orm):
        
        # Deleting model 'MetaInfo'
        db.delete_table('web_metainfo')
        
        # Deleting field 'Package.metainfo'
        db.delete_column('web_package', 'metainfo_id')
        
        # Adding field 'Package.update_id'
        db.add_column('web_package', 'update_id', orm['web.package:update_id'])
        
    
    
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
            'update_id': ('django.db.models.fields.CharField', [], {'max_length': '50'})
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
