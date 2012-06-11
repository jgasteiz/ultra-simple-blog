# -*- coding: utf-8 -*-
from google.appengine.api import users
from google.appengine.ext import db
from simpleblog.utils import uuslug as slugify
from simpleblog.forms import EntryForm
from django.contrib import messages

class ContextManager():
	def get_context(self, type):
		"""Return a contexts based on authenticated user"""
		# Sets login/logout urls
		if users.get_current_user():
			url = users.create_logout_url('/')
			url_linktext = 'Logout'
			form = EntryForm()
		else:
			url = users.create_login_url('/')
			url_linktext = 'Login'
			form = ''
		context = {
			'url': url,
			'url_linktext': url_linktext,
			'current_user': users.get_current_user(),
			'form': form,
		}
		return context

class EntryManager():
	"""Manager for the Entry model"""
	def author(self, author):
		"""Need to find a better way to do this"""
		entries_qs = Entry.all().order('-date')
		entry_list = []
		for e in entries_qs:
			if e.author.nickname() == author:
				entry_list.append(e)
		return entry_list

class Entry(db.Model):
	"""
    Stores a single blog entry

    """
	author = db.UserProperty()
	title = db.StringProperty()
	slug = db.StringProperty()
	content = db.TextProperty()
	moderated = db.StringProperty(default="")
	date = db.DateTimeProperty(auto_now_add=True)

	objects = EntryManager()
	context = ContextManager()
	
	def __unicode__(self):
		"""Returns the Entry title"""
		return self.title

	def put(self, form, request):
		"""Saves an Entry or creates a new one"""
		if not form.is_valid():
			messages.add_message(request, messages.ERROR, "Not a valid entry")
			return False
		if not users.get_current_user():
			messages.add_message(request, messages.ERROR, "Must be logged in")
			return False
		if not self.author:
			self.author = users.get_current_user()
		if self.author != users.get_current_user():
			if users.is_current_user_admin():
				self.moderated = "moderated"
			else:
				messages.add_message(request, messages.ERROR, "You are not the owner!")
				return False
		cd = form.cleaned_data
		self.title = cd['title']
		self.content = cd['content']
		if not self.slug:
			self.slug = slugify(self.title, instance=self)
		super(Entry, self).put()

	def delete(self, request):
		"""Deletes an Entry"""
		if not users.get_current_user():
			messages.add_message(request, messages.ERROR, "Must be logged in")
			return False
		if self.author != users.get_current_user() and not users.is_current_user_admin():
			messages.add_message(request, messages.ERROR, "You are not the owner!")
			return False
		super(Entry, self).delete()
