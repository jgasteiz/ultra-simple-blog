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
		return Entry.objects.published()

	def post(self, request, *args, **kwargs):
		"""
		If everything's correct, creates/edits an entry
		"""
		form = EntryForm(request.POST)
		e = Entry.get_by_id(int(request.POST['id']))
		if not e:
			e = Entry()
		if e.is_valid(form=form, request=request):
			cd = form.cleaned_data
			e.title = cd['title']
			e.content = cd['content']
			e.put()
		return HttpResponseRedirect("/")
	
	def get_context_data(self, **kwargs):
		user_context = Entry.users.user_context()
		context = super(BlogView, self).get_context_data(**kwargs)
		context.update(user_context)
		context.update({'blocks': {'footer': 1},})
		return context


class BlogPostView(ListView):
	"""
	Single page for an entry
	"""
	context_object_name = 'entry_list'
	template_name = 'simpleblog/index.html'

	def get_queryset(self):
		return Entry.objects.single(self.kwargs['slug'])

	def get_context_data(self, **kwargs):
		user_context = Entry.users.user_context()
		context = super(BlogPostView, self).get_context_data(**kwargs)
		context.update(user_context)
		context.update({'blocks': {},})
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
