# -*- coding: utf-8 -*-
from django.http import HttpResponse, HttpResponseRedirect
from django.template.defaultfilters import slugify
from django.shortcuts import render
from django.contrib import messages

from django.views.generic import DetailView, ListView

from google.appengine.api import users
from simpleblog.models import Entry
from simpleblog.forms import EntryForm

def home(request):
	"""
	Main page. Loads all the entries, ordered by date.
	If request method is post, there may be creating or editing an entry.
	"""
	# Check for current user
	if users.get_current_user():
		url = users.create_logout_url('/')
		url_linktext = 'Logout'
	else:
		url = users.create_login_url('/')
		url_linktext = 'Login'

	entries_qs = Entry.all().order('-date')
	entries_list = []
	for e in entries_qs:
		editable = users.is_current_user_admin() or e.author == users.get_current_user()
		entries_list.append({ 'editable': str(editable), 'entry': e })

	template_values = {
		'entries': entries_list,
		'url': url,
		'is_admin': users.is_current_user_admin(),
		'url_linktext': url_linktext,
		'current_user': users.get_current_user(),
		'form': EntryForm(),
		}
	return render(request, 'simpleblog/index.html', template_values)

def new_entry(request):
	"""
	If everything's correct, creates a new entry
	"""
	if request.method == 'POST':
		form = EntryForm(request.POST)
		if form.is_valid():
			cd = form.cleaned_data
			Entry(
				title = cd['title'],
				content = cd['content'],
				).put()
		else:
			messages.add_message(request, messages.ERROR, "Not a valid entry")
	return HttpResponseRedirect("/")

def edit_entry(request):
	"""
	If everything's correct and the user is the owner (or admin), it's edited
	"""
	if request.method == 'POST':
		entry = Entry.get_by_id(int(request.POST['id']))
		form = EntryForm(request.POST)
		if form.is_valid() and (entry.own(users.get_current_user()) or users.is_current_user_admin()):
			cd = form.cleaned_data
			entry.title = cd['title']
			entry.content = cd['content']
			entry.put()
		else:
			if not entry.own(users.get_current_user()):
				messages.add_message(request, messages.ERROR, "You are not the owner!")
			else:
				messages.add_message(request, messages.ERROR, "Not a valid entry")
	return HttpResponseRedirect("/")

def delete_entry(request, id):
	"""
	Deletes an entry if the user is the owner or the admin
	"""
	entry = Entry.get_by_id(int(id))
	if entry.own(users.get_current_user()) or users.is_current_user_admin():
		entry.delete()
	else:
		messages.add_message(request, messages.ERROR, "You are not the owner!")
	return HttpResponseRedirect("/")


# class EntriesDetailView(ListView):
# 	context_object_name = "entry_list"
# 	template_name = "simpleblog/entry_list.html"
# 	def get_queryset(self):
# 		return Entry.all()
