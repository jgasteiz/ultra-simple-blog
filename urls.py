from django.conf.urls.defaults import *

from core.views import home, new_entry, delete_entry, edit_entry

handler500 = 'djangotoolbox.errorviews.server_error'

urlpatterns = patterns('',
	url(r'^_ah/warmup$', 'djangoappengine.views.warmup'),
	url(r'new_entry', new_entry, name='new_entry'),
	url(r'edit_entry/(?P<id>\w+)', edit_entry, name='edit_entry'),
	url(r'delete_entry/(?P<id>\w+)', delete_entry, name='delete_entry'),
	url(r'^$', home, name='home'),
)