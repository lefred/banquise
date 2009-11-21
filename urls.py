from django.conf.urls.defaults import *
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^banquise/', include('banquise.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
    (r'^web/', include('banquise.web.urls')),
    (r'^media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': '/home/sejo/playground/banquise/web/media', 'show_indexes': True}),

    (r'^$', 'banquise.web.views.index'),

)
