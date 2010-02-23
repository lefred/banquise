from django.db import models
import datetime


class Customer(models.Model):
    name = models.CharField(max_length=150)
    contact = models.CharField(max_length=150)
    email = models.CharField(max_length=150) 
    
    def __unicode__(self):
        return self.name

class Contract(models.Model):
    start_date = models.DateField('starting date')
    end_date = models.DateField('ending date')
    days_left = lambda x:  (x.end_date - datetime.date.today()).days
    customer = models.ForeignKey(Customer)
    license = models.CharField(max_length=32)
    hosts = models.ManyToManyField('Host',
            symmetrical=False,
            related_name='C_h_H')

    def _packages_to_update(self):
        tot=0
        for host in self.hosts.all():
            tot = tot + int(host.packages_to_update())
        return tot
    packages_to_update = property(fget=_packages_to_update)

    def __str__(self):
        return " (" + str(self.start_date) + " -> " + str(self.end_date) + ")"

    class Meta:
        get_latest_by = 'end_date'

class Host(models.Model):
    name = models.CharField(max_length=250)
    ip = models.CharField(max_length=15)
    public_ip = models.CharField(max_length=15)
    release = models.CharField(max_length=100)
    hash = models.CharField(max_length=32)
    packages_to_update = lambda x:  ServerPackages.objects.filter(host=x,package_installed=0,package_skipped=0).count()

    def __str__(self):
        return self.name

class MetaInfo(models.Model):
    updateid = models.CharField(max_length=50)
    status = models.CharField(max_length=20)
    type = models.CharField(max_length=20)
    description = models.TextField()
    
    def __str__(self):
        return str(self.updateid)

class MetaBug(models.Model):
    bugid = models.CharField(max_length=50)
    href = models.CharField(max_length=250)
    type = models.CharField(max_length=20)
    title = models.TextField()
    metainfo=models.ForeignKey(MetaInfo, null=True)
    
    def __str__(self):
        return str(self.bugid)


class Package(models.Model):
    name = models.CharField(max_length=80)
    arch = models.CharField(max_length=10)
    version = models.CharField(max_length=50)
    release = models.CharField(max_length=50)
    repo = models.CharField(max_length=50,blank=True)
    type = models.CharField(max_length=15,blank=True)
    metainfo=models.ForeignKey(MetaInfo,null=True,blank=True)
    class Meta:
        unique_together = ('name', 'arch', 'version', 'release',)

    def __str__(self):
        return self.name + '-' + self.arch + '.' + self.version + '.' + self.release

class ServerPackages(models.Model):
    package = models.ForeignKey(Package)
    host = models.ForeignKey(Host)
    package_installed = models.BooleanField()
    date_available = models.DateTimeField(blank=True,null=True)
    date_installed = models.DateTimeField(blank=True,null=True)
    date_synced = models.DateTimeField(blank=True,null=True)
    to_install = models.BooleanField() 
    package_skipped = models.BooleanField()
    new_install = models.BooleanField()
    removed = models.BooleanField()
    
    def __str__(self):
        return str(self.package) + '-' + str(self.host)

