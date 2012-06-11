# -*- coding: utf-8 -*-
from django.conf.urls.defaults import url, patterns
from simpleblog.views import *

handler500 = 'djangotoolbox.errorviews.server_error'

urlpatterns = patterns('',
	url(r'^_ah/warmup$', 'djangoappengine.views.warmup'),
	url(r'^$', 
		EntryListView.as_view(),
		name='entry_list'),
	url(r'single/(?P<slug>[\w-]+)/$',
		EntryDetailView.as_view(),
		name='post'),

	url(r'new_entry/', 
		EntryCreateView.as_view(),
		name='new_entry'),
	url(r'edit_entry/', 
		EntryEditView.as_view(),
		name='edit_entry'),
	url(r'delete_entry/', 
		EntryDeleteView.as_view(),
		name='delete_entry'),	
)