from django.contrib import admin
from banquise.web.models import Customer
from banquise.web.models import Host
from banquise.web.models import Package
from banquise.web.models import Contract

admin.site.register(Customer)
admin.site.register(Host)
admin.site.register(Contract)
admin.site.register(Package)

