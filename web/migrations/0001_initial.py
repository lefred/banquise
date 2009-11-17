
from south.db import db
from django.db import models
from banquise.web.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'Contract'
        db.create_table('web_contract', (
            ('id', orm['web.Contract:id']),
            ('start_date', orm['web.Contract:start_date']),
            ('end_date', orm['web.Contract:end_date']),
            ('customer', orm['web.Contract:customer']),
        ))
        db.send_create_signal('web', ['Contract'])
        
        # Adding model 'Package'
        db.create_table('web_package', (
            ('id', orm['web.Package:id']),
            ('name', orm['web.Package:name']),
            ('arch', orm['web.Package:arch']),
            ('ver', orm['web.Package:ver']),
            ('rel', orm['web.Package:rel']),
        ))
        db.send_create_signal('web', ['Package'])
        
        # Adding model 'ServerPackages'
        db.create_table('web_serverpackages', (
            ('id', orm['web.ServerPackages:id']),
            ('package', orm['web.ServerPackages:package']),
            ('host', orm['web.ServerPackages:host']),
            ('package_installed', orm['web.ServerPackages:package_installed']),
            ('date_available', orm['web.ServerPackages:date_available']),
            ('date_installed', orm['web.ServerPackages:date_installed']),
            ('to_install', orm['web.ServerPackages:to_install']),
        ))
        db.send_create_signal('web', ['ServerPackages'])
        
        # Adding model 'Host'
        db.create_table('web_host', (
            ('id', orm['web.Host:id']),
            ('name', orm['web.Host:name']),
            ('ip', orm['web.Host:ip']),
            ('public_ip', orm['web.Host:public_ip']),
            ('release', orm['web.Host:release']),
            ('hash', orm['web.Host:hash']),
        ))
        db.send_create_signal('web', ['Host'])
        
        # Adding model 'Customer'
        db.create_table('web_customer', (
            ('id', orm['web.Customer:id']),
            ('name', orm['web.Customer:name']),
        ))
        db.send_create_signal('web', ['Customer'])
        
        # Adding model 'ServerContracts'
        db.create_table('web_servercontracts', (
            ('id', orm['web.ServerContracts:id']),
            ('contract', orm['web.ServerContracts:contract']),
            ('server', orm['web.ServerContracts:server']),
        ))
        db.send_create_signal('web', ['ServerContracts'])
        
    
    
    def backwards(self, orm):
        
        # Deleting model 'Contract'
        db.delete_table('web_contract')
        
        # Deleting model 'Package'
        db.delete_table('web_package')
        
        # Deleting model 'ServerPackages'
        db.delete_table('web_serverpackages')
        
        # Deleting model 'Host'
        db.delete_table('web_host')
        
        # Deleting model 'Customer'
        db.delete_table('web_customer')
        
        # Deleting model 'ServerContracts'
        db.delete_table('web_servercontracts')
        
    
    
    models = {
        'web.contract': {
            'customer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['web.Customer']"}),
            'end_date': ('django.db.models.fields.DateField', [], {}),
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
            'rel': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'ver': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'web.servercontracts': {
            'contract': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['web.Contract']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'server': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['web.Host']"})
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
