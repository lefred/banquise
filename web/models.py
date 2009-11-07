from django.db import models
import datetime



class Customer(models.Model):
    name = models.CharField(max_length=150)

    def __unicode__(self):
       return self.name

class Contract(models.Model):
    start_date = models.DateField('starting date')
    end_date = models.DateField('ending date')
    customer = models.ForeignKey(Customer)

    def __unicode__(self):
       return " (" + str(self.start_date) + " -> " + str(self.end_date) + ")"

class Host(models.Model):
    name = models.CharField(max_length=250)
    ip = models.CharField(max_length=15)
    public_ip = models.CharField(max_length=15)
    release = models.CharField(max_length=100)
    hash = models.CharField(max_length=32)

    def __unicode__(self):
       return self.name

class Package(models.Model):
    name = models.CharField(max_length=250)
    arch = models.CharField(max_length=50)
    ver = models.CharField(max_length=50)
    rel = models.CharField(max_length=50)

    def __unicode__(self):
       return self.name + '-' + self.arch + '.' + self.ver + '.' + self.rel
 
class ServerContracts(models.Model):
    contract = models.ForeignKey(Contract)
    server = models.ForeignKey(Host) 

class ServerPackages(models.Model):
    package = models.ForeignKey(Package)
    host = models.ForeignKey(Host)
    package_installed = models.BooleanField()
    date_available = models.DateTimeField()
    date_installed = models.DateTimeField()
    to_install = models.BooleanField() 
