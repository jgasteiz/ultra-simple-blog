# -*- coding: utf-8 -*-
from django.conf.urls.defaults import url, patterns
from simpleblog.views import BlogView, BlogPostView

handler500 = 'djangotoolbox.errorviews.server_error'

urlpatterns = patterns('',
	url(r'^_ah/warmup$', 'djangoappengine.views.warmup'),
	url(r'^$', 
		BlogView.as_view(),
		name='blog'),
	url(r'new_entry/', 
		BlogView.as_view(),
		name='new_entry'),
	url(r'edit_entry/', 
		BlogView.as_view(),
		name='edit_entry'),
	url(r'delete_entry/', 
		BlogView.as_view(),
		name='delete_entry'),
	url(r'(?P<slug>[\w-]+)/$',
		BlogPostView.as_view(),
		name='post'),
)
