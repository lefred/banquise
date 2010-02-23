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
    (r'^list/metainfo/(?P<package_id>\d+)/(?P<metainfo_id>\d+)/$', 'list_metainfo'),
    (r'^list/hosts/$', 'list_hosts'),
    (r'^list/hosts/(?P<contract_id>\d+)/$', 'list_hosts'),
    (r'^list/packages/$', 'form_packages'),
    (r'^list/packages/(?P<host_id>\d+)/$', 'list_packages'),
    (r'^customer/(?P<customer_id>\d+)/$','details_customer'),
    (r'^serverpackage/(?P<package_id>\d+)/$','server_package'),
    (r'^accounts/logout/$','logout_view'),
    (r'^json/setup/$','call_setup'),
    (r'^json/test/$','call_test'),
    (r'^json/metabug/$','call_send_metabug'),
    (r'^json/metainfo/$','call_send_metainfo'),
    (r'^json/set_release/$','call_set_release'),
    (r'^json/update/$','call_send_update'),
    (r'^json/sync/$','call_send_sync'),
    (r'^json/packdone/$','call_packs_done'),
    (r'^json/addpack/$','call_send_list'),
    (r'^json/install/$','call_send_install'),
)
