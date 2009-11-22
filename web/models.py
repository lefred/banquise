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
    license = models.CharField(max_length=32)
    hosts = models.ManyToManyField('Host',
            symmetrical=False,
            related_name='C_h_H')

    def __str__(self):
       return " (" + str(self.start_date) + " -> " + str(self.end_date) + ")"

class Host(models.Model):
    name = models.CharField(max_length=250)
    ip = models.CharField(max_length=15)
    public_ip = models.CharField(max_length=15)
    release = models.CharField(max_length=100)
    hash = models.CharField(max_length=32)

    def __str__(self):
       return self.name

class Package(models.Model):
    name = models.CharField(max_length=80)
    arch = models.CharField(max_length=10)
    version = models.CharField(max_length=50)
    release = models.CharField(max_length=50)

    class Meta:
        unique_together = ('name', 'arch', 'version', 'release',)

    def __str__(self):
       return self.name + '-' + self.arch + '.' + self.version + '.' + self.release

class ServerPackages(models.Model):
    package = models.ForeignKey(Package)
    host = models.ForeignKey(Host)
    package_installed = models.BooleanField()
    date_available = models.DateTimeField()
    date_installed = models.DateTimeField()
    to_install = models.BooleanField() 
