
from south.db import db
from django.db import models
from banquise.web.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Changing field 'Contract.license'
        # (to signature: django.db.models.fields.CharField(max_length=32, null=True))
        db.alter_column('web_contract', 'license', orm['web.contract:license'])
        
        # Changing field 'Package.repo'
        # (to signature: django.db.models.fields.CharField(max_length=50, null=True, blank=True))
        db.alter_column('web_package', 'repo', orm['web.package:repo'])
        
        # Changing field 'Package.version'
        # (to signature: django.db.models.fields.CharField(max_length=50, null=True))
        db.alter_column('web_package', 'version', orm['web.package:version'])
        
        # Changing field 'Package.release'
        # (to signature: django.db.models.fields.CharField(max_length=50, null=True))
        db.alter_column('web_package', 'release', orm['web.package:release'])
        
        # Changing field 'Package.type'
        # (to signature: django.db.models.fields.CharField(max_length=15, null=True, blank=True))
        db.alter_column('web_package', 'type', orm['web.package:type'])
        
        # Changing field 'MetaInfo.status'
        # (to signature: django.db.models.fields.CharField(max_length=20, null=True))
        db.alter_column('web_metainfo', 'status', orm['web.metainfo:status'])
        
        # Changing field 'MetaInfo.description'
        # (to signature: django.db.models.fields.TextField(null=True))
        db.alter_column('web_metainfo', 'description', orm['web.metainfo:description'])
        
        # Changing field 'MetaInfo.updateid'
        # (to signature: django.db.models.fields.CharField(max_length=50, null=True))
        db.alter_column('web_metainfo', 'updateid', orm['web.metainfo:updateid'])
        
        # Changing field 'Customer.contact'
        # (to signature: django.db.models.fields.CharField(max_length=150, null=True))
        db.alter_column('web_customer', 'contact', orm['web.customer:contact'])
        
        # Changing field 'Customer.email'
        # (to signature: django.db.models.fields.CharField(max_length=150, null=True))
        db.alter_column('web_customer', 'email', orm['web.customer:email'])
        
    
    
    def backwards(self, orm):
        
        # Changing field 'Contract.license'
        # (to signature: django.db.models.fields.CharField(max_length=32))
        db.alter_column('web_contract', 'license', orm['web.contract:license'])
        
        # Changing field 'Package.repo'
        # (to signature: django.db.models.fields.CharField(max_length=50, blank=True))
        db.alter_column('web_package', 'repo', orm['web.package:repo'])
        
        # Changing field 'Package.version'
        # (to signature: django.db.models.fields.CharField(max_length=50))
        db.alter_column('web_package', 'version', orm['web.package:version'])
        
        # Changing field 'Package.release'
        # (to signature: django.db.models.fields.CharField(max_length=50))
        db.alter_column('web_package', 'release', orm['web.package:release'])
        
        # Changing field 'Package.type'
        # (to signature: django.db.models.fields.CharField(max_length=15, blank=True))
        db.alter_column('web_package', 'type', orm['web.package:type'])
        
        # Changing field 'MetaInfo.status'
        # (to signature: django.db.models.fields.CharField(max_length=20))
        db.alter_column('web_metainfo', 'status', orm['web.metainfo:status'])
        
        # Changing field 'MetaInfo.description'
        # (to signature: django.db.models.fields.TextField())
        db.alter_column('web_metainfo', 'description', orm['web.metainfo:description'])
        
        # Changing field 'MetaInfo.updateid'
        # (to signature: django.db.models.fields.CharField(max_length=50))
        db.alter_column('web_metainfo', 'updateid', orm['web.metainfo:updateid'])
        
        # Changing field 'Customer.contact'
        # (to signature: django.db.models.fields.CharField(max_length=150))
        db.alter_column('web_customer', 'contact', orm['web.customer:contact'])
        
        # Changing field 'Customer.email'
        # (to signature: django.db.models.fields.CharField(max_length=150))
        db.alter_column('web_customer', 'email', orm['web.customer:email'])
        
    
    
    models = {
        'web.changelog': {
            'authorversion': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'package': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['web.Package']"}),
            'timestamp': ('django.db.models.fields.IntegerField', [], {})
        },
        'web.contract': {
            'customer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['web.Customer']"}),
            'end_date': ('django.db.models.fields.DateField', [], {}),
            'hosts': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['web.Host']", 'symmetrical': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'license': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True'}),
            'start_date': ('django.db.models.fields.DateField', [], {})
        },
        'web.customer': {
            'contact': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True'}),
            'email': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True'}),
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
            'updateid': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'})
        },
        'web.package': {
            'Meta': {'unique_together': "(('name', 'arch', 'version', 'release'),)"},
            'arch': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'metainfo': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['web.MetaInfo']", 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'release': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'}),
            'repo': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'version': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'})
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
