from django.conf.urls.defaults import *
from banquise.web.models import Customer,Host,Package

info_dict = {
    'queryset': Customer.objects.all(),
}


# Uncomment the next two lines to enable the admin:
#from django.contrib import admin
#admin.autodiscover()

urlpatterns = patterns('banquise.web.views',
    # Example:
    # (r'^banquise/', include('banquise.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    #(r'^$', 'django.views.generic.list_detail.object_list', info_dict),
    (r'^list/customers/$', 'list_customers'),
    (r'^list/customers/$', 'list_customers'),
    (r'^list/hosts/$', 'list_hosts'),
    (r'^customer/(?P<customer_id>\d+)/$','details_customer'),
)
