# -*- coding: utf-8 -*-
from django.http import HttpResponse, HttpResponseRedirect
from django.template.defaultfilters import slugify
from django.shortcuts import render
from django.contrib import messages

from django.views.generic import ListView, RedirectView

from google.appengine.ext import db
from google.appengine.api import users
from simpleblog.models import Entry
from simpleblog.forms import EntryForm

class BlogView(ListView):
	"""
	Main page. Loads all the entries, ordered by date.
	If request method is post, there may be creating or editing an entry.
	"""
	paginate_by = 5
	context_object_name = 'entry_list'
	template_name = 'simpleblog/index.html'

	def get_queryset(self):
		entries_qs = Entry.all().order('-date')
		entry_list = []
		for e in entries_qs:
			editable = users.is_current_user_admin() or e.author == users.get_current_user()
			if editable:
				e.id = str(e.key().id())
			entry_list.append({ 'editable': str(editable), 'entry': e })
		return entry_list

	def post(self, request, *args, **kwargs):
		"""
		If everything's correct, creates/edits an entry
		"""
		form = EntryForm(request.POST)
		if form.is_valid() and users.get_current_user():
			cd = form.cleaned_data
			e = Entry.get_by_id(int(request.POST['id']))
			if e:
				if e.own(users.get_current_user()):
					e.title = cd['title']
					e.content = cd['content']
					e.put()
				else:
					messages.add_message(request, messages.ERROR, "You are not the owner!")
			else:
				Entry(
					title = cd['title'],
					content = cd['content'],
					).put()
		else:
			if not form.is_valid():
				messages.add_message(request, messages.ERROR, "Not a valid entry")
			elif not users.get_current_user():
				messages.add_message(request, messages.ERROR, "Must be logged in")
		return HttpResponseRedirect("/")
	
	def get_context_data(self, **kwargs):
		# Sets login/logout urls
		if users.get_current_user():
			url = users.create_logout_url('/')
			url_linktext = 'Logout'
		else:
			url = users.create_login_url('/')
			url_linktext = 'Login'

		context = super(BlogView, self).get_context_data(**kwargs)
		context.update({
			'url': url,
			'url_linktext': url_linktext,
			'is_admin': users.is_current_user_admin(),
			'current_user': users.get_current_user(),
			'form': EntryForm(),
			'blocks': {'footer': 1},
		})
		return context


class BlogPostView(ListView):
	"""
	Single page for an entry
	"""
	context_object_name = 'entry_list'
	template_name = 'simpleblog/index.html'

	def get_queryset(self):
		e = Entry.all().filter('slug =', self.kwargs['slug']).get()
		editable = users.is_current_user_admin() or e.author == users.get_current_user()
		if editable:
			e.id = str(e.key().id())
		return [{"entry": e, "editable": str(editable)}]

	def get_context_data(self, **kwargs):
		# Sets login/logout urls
		if users.get_current_user():
			url = users.create_logout_url('/')
			url_linktext = 'Logout'
		else:
			url = users.create_login_url('/')
			url_linktext = 'Login'

		context = super(BlogPostView, self).get_context_data(**kwargs)
		context.update({
			'url': url,
			'url_linktext': url_linktext,
			'is_admin': users.is_current_user_admin(),
			'current_user': users.get_current_user(),
			'form': EntryForm(),
			'blocks': {},
		})
		return context

class DeletePostView(RedirectView):
	"""
	For deleting a post
	"""
	def get(self, request):
		entry = Entry.get_by_id(int(request.GET['entry']))
		if entry.own(users.get_current_user()) or users.is_current_user_admin():
			entry.delete()
		else:
			messages.add_message(request, messages.ERROR, "You are not the owner!")
		return HttpResponseRedirect("/")
