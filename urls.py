from django.conf.urls.defaults import *

from core.views import home, delete_entry

handler500 = 'djangotoolbox.errorviews.server_error'

urlpatterns = patterns('',
	url(r'^_ah/warmup$', 'djangoappengine.views.warmup'),
	url(r'delete_entry/(?P<id>\w+)', delete_entry, name='delete_entry'),
	url(r'^$', home, name='home'),
)