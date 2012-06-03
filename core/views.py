# -*- coding: utf-8 -*-
from django.http import HttpResponse, HttpResponseRedirect
from django.template.defaultfilters import slugify
from django.shortcuts import render

from google.appengine.api import users
from core.models import Entry

def home(request):
	"""
	Main function
	"""
	entries_query = Entry.all().order('-date')
	entries = entries_query.fetch(10)

	if users.get_current_user():
		username = users.get_current_user()
		url = users.create_logout_url('/')
		url_linktext = 'Logout'
	else:
		username = ''
		url = users.create_login_url('/')
		url_linktext = 'Login'

	template_values = {
		'entries': entries,
		'url': url,
		'url_linktext': url_linktext,
		'username': username,
		}
	return render(request, 'core/index.html', template_values)

def new_entry(request):
	"""
	Creates a new entry
	"""
	if request.method == 'POST':
		entry = Entry()
		entry.title = request.POST['title']
		entry.slug = slugify(entry.title)
		entry.content = request.POST['content']
		if users.get_current_user():
			entry.author = users.get_current_user()
		if entry.content != '' and entry.title != '':
			entry.put()
	return HttpResponseRedirect("/")

def delete_entry(request, id):
	"""
	Deletes an entry
	"""
	Entry.get_by_id(int(id)).delete()
	return HttpResponseRedirect("/")

def edit_entry(request, id):
	"""
	Edits an entry
	"""
	if request.method == 'POST':
		entry = Entry.get_by_id(int(id))
		entry.title = request.POST['title']
		entry.content = request.POST['content']
		if users.get_current_user():
			entry.author = users.get_current_user()
		if entry.content != '' and entry.title != '':
			entry.put()
	return HttpResponseRedirect("/")


