
from south.db import db
from django.db import models
from banquise.web.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding field 'Package.release'
        db.add_column('web_package', 'release', orm['web.package:release'])
        
        # Adding ManyToManyField 'Contract.hosts'
        db.create_table('web_contract_hosts', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('contract', models.ForeignKey(orm.Contract, null=False)),
            ('host', models.ForeignKey(orm.Host, null=False))
        ))
        
        # Adding field 'Package.version'
        db.add_column('web_package', 'version', orm['web.package:version'])
        
        # Deleting field 'Package.ver'
        db.delete_column('web_package', 'ver')
        
        # Deleting field 'Package.rel'
        db.delete_column('web_package', 'rel')
        
        # Deleting model 'servercontracts'
        db.delete_table('web_servercontracts')
        
    
    
    def backwards(self, orm):
        
        # Deleting field 'Package.release'
        db.delete_column('web_package', 'release')
        
        # Dropping ManyToManyField 'Contract.hosts'
        db.delete_table('web_contract_hosts')
        
        # Deleting field 'Package.version'
        db.delete_column('web_package', 'version')
        
        # Adding field 'Package.ver'
        db.add_column('web_package', 'ver', orm['web.package:ver'])
        
        # Adding field 'Package.rel'
        db.add_column('web_package', 'rel', orm['web.package:rel'])
        
        # Adding model 'servercontracts'
        db.create_table('web_servercontracts', (
            ('id', orm['web.package:id']),
            ('contract', orm['web.package:contract']),
            ('server', orm['web.package:server']),
        ))
        db.send_create_signal('web', ['servercontracts'])
        
    
    
    models = {
        'web.contract': {
            'customer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['web.Customer']"}),
            'end_date': ('django.db.models.fields.DateField', [], {}),
            'hosts': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['web.Host']", 'symmetrical': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
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
            'arch': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'release': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'}),
            'version': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'})
        },
        'web.serverpackages': {
            'date_available': ('django.db.models.fields.DateTimeField', [], {}),
            'date_installed': ('django.db.models.fields.DateTimeField', [], {}),
            'host': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['web.Host']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'package': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['web.Package']"}),
            'package_installed': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'to_install': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'})
        }
    }
    
    complete_apps = ['web']
