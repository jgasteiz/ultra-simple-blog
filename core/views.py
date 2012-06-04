# -*- coding: utf-8 -*-
from django.http import HttpResponse, HttpResponseRedirect
from django.template.defaultfilters import slugify
from django.shortcuts import render

from google.appengine.api import users
from core.models import Entry
from core.forms import EntryForm

def home(request):
	"""
	Main page. Loads all the entries, ordered by date.
	If request method is post, there may be creating or editing an entry.
	"""
	# First of all, check for current user
	if users.get_current_user():
		current_user = users.get_current_user()
		url = users.create_logout_url('/')
		url_linktext = 'Logout'
	else:
		current_user = ''
		url = users.create_login_url('/')
		url_linktext = 'Login'

	errors = []
	if request.method == 'POST':
		if request.POST['id'] != "-1":
			entry = Entry.get_by_id(int(request.POST['id']))
		else:
			entry = Entry()
			entry.author = users.get_current_user()
		form = EntryForm(request.POST)
		if form.is_valid() and entry.own(current_user):
			cd = form.cleaned_data
			entry.title = cd['title']
			entry.slug = slugify(entry.title)
			entry.content = cd['content']
			entry.put()
			return HttpResponseRedirect("/")
		else:
			if not entry.own(current_user):
				errors.append({'message': "You are not the owner!"})
			else:
				errors.append({'message': "Not a valid entry"})
	form = EntryForm()
	template_values = {
		'entries': Entry.all().order('-date'),
		'url': url,
		'url_linktext': url_linktext,
		'current_user': current_user,
		'form': form,
		'errors': errors
		}
	return render(request, 'core/index.html', template_values)


def delete_entry(request, id):
	"""
	Deletes an entry
	"""
	errors = []
	entry = Entry.get_by_id(int(id))
	if entry.own(users.get_current_user()):
		entry.delete()
	else:
		errors.append({'message': "You are not the owner!"})
	return HttpResponseRedirect("/")
