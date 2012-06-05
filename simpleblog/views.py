# -*- coding: utf-8 -*-
from django.http import HttpResponse, HttpResponseRedirect
from django.template.defaultfilters import slugify
from django.shortcuts import render
from django.contrib import messages

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
		current_user = users.get_current_user()
		url = users.create_logout_url('/')
		url_linktext = 'Logout'
	else:
		current_user = ''
		url = users.create_login_url('/')
		url_linktext = 'Login'

	template_values = {
		'entries': Entry.all().order('-date'),
		'url': url,
		'url_linktext': url_linktext,
		'current_user': current_user,
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
				author = users.get_current_user(),
				).put()
		else:
			messages.add_message(request, messages.ERROR, "Not a valid entry")
	return HttpResponseRedirect("/")

def edit_entry(request):
	"""
	If everything's correct and the entry owner is the user trying to edit it, 
	edits the entry
	"""
	if request.method == 'POST':
		entry = Entry.get_by_id(int(request.POST['id']))
		form = EntryForm(request.POST)
		if form.is_valid() and entry.own(users.get_current_user()):
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
	Deletes an entry if the user is the owner
	"""
	entry = Entry.get_by_id(int(id))
	if entry.own(users.get_current_user()):
		entry.delete()
	else:
		messages.add_message(request, messages.ERROR, "You are not the owner!")
	return HttpResponseRedirect("/")
