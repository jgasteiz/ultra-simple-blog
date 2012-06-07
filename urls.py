from django.conf.urls.defaults import url, patterns, include

from simpleblog.views import home, new_entry, edit_entry, delete_entry#, EntriesDetailView
from django.views.generic import ListView, DetailView
from simpleblog.models import Entry

handler500 = 'djangotoolbox.errorviews.server_error'

urlpatterns = patterns('',
	url(r'^_ah/warmup$', 'djangoappengine.views.warmup'),
	url(r'new_entry/', new_entry, name='new_entry'),
	url(r'edit_entry/', edit_entry, name='edit_entry'),
	url(r'delete_entry/(?P<id>\w+)', delete_entry, name='delete_entry'),
	url(r'^$', home, name='home'),
	# url(r'^entries/$', EntriesDetailView.as_view()),
)
