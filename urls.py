from django.conf.urls.defaults import url, patterns, include

from simpleblog.views import BlogView, BlogPostView, new_entry, edit_entry, delete_entry

handler500 = 'djangotoolbox.errorviews.server_error'

urlpatterns = patterns('',
	url(r'^_ah/warmup$', 'djangoappengine.views.warmup'),
	url(r'^$', 
		BlogView.as_view(),
		name='blog'),
	url(r'new_entry/', new_entry, name='new_entry'),
	url(r'edit_entry/', edit_entry, name='edit_entry'),
	url(r'delete_entry/(?P<id>\w+)', delete_entry, name='delete_entry'),
	url(r'(?P<slug>[\w-]+)/$',
        BlogPostView.as_view(),
        name='post'),
)
