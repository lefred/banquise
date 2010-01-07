
from south.db import db
from django.db import models
from banquise.web.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding field 'ServerPackages.package_skipped'
        db.add_column('web_serverpackages', 'package_skipped', orm['web.serverpackages:package_skipped'])
        
        # Changing field 'ServerPackages.date_available'
        # (to signature: django.db.models.fields.DateTimeField(null=True, blank=True))
        db.alter_column('web_serverpackages', 'date_available', orm['web.serverpackages:date_available'])
        
        # Changing field 'ServerPackages.date_installed'
        # (to signature: django.db.models.fields.DateTimeField(null=True, blank=True))
        db.alter_column('web_serverpackages', 'date_installed', orm['web.serverpackages:date_installed'])
        
    
    
    def backwards(self, orm):
        
        # Deleting field 'ServerPackages.package_skipped'
        db.delete_column('web_serverpackages', 'package_skipped')
        
        # Changing field 'ServerPackages.date_available'
        # (to signature: django.db.models.fields.DateTimeField())
        db.alter_column('web_serverpackages', 'date_available', orm['web.serverpackages:date_available'])
        
        # Changing field 'ServerPackages.date_installed'
        # (to signature: django.db.models.fields.DateTimeField())
        db.alter_column('web_serverpackages', 'date_installed', orm['web.serverpackages:date_installed'])
        
    
    
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
        'web.package': {
            'Meta': {'unique_together': "(('name', 'arch', 'version', 'release'),)"},
            'arch': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'release': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'version': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'web.serverpackages': {
            'date_available': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'date_installed': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'host': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['web.Host']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'package': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['web.Package']"}),
            'package_installed': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'package_skipped': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'to_install': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'})
        }
    }
    
    complete_apps = ['web']
