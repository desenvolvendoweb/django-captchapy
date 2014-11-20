try:
    from django.conf.urls.defaults import include, patterns, url
except:
    # Django 1.6.2
    from django.conf.urls import include, patterns, url
from django.conf import settings

import os

MODPATH = os.path.abspath(os.path.dirname(__file__))

urlpatterns  = patterns('',
    url(r'^(?P<path>.*)$' , 'django.views.static.serve',
        {'document_root': MODPATH}),
)
