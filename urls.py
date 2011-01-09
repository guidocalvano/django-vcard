from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^vCardProject/enterVCard/', 'vCard.views.vCardForm' ),
    (r'^testVCard/', 'vCard.views.testVCardForm' ),
    (r'^vCardProject/hCard/', 'vCard.views.hCard' ),
    (r'^admin/vCard/upload/loadFile/$', 'vCard.admin_views.loadFile'),    
    (r'^admin/vCard/upload/$', 'vCard.admin_views.select'),    
    # (r'^vCardProject/', include('vCardProject.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
)
