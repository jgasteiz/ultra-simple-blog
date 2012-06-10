# -*- coding: utf-8 -*-
from google.appengine.api import users
from google.appengine.ext import db
from simpleblog.managers import *
from simpleblog.utils import uuslug as slugify
from simpleblog.forms import EntryForm
from django.contrib import messages
import re

class UserManager():
	def user_context(self):
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
			'is_admin': users.is_current_user_admin(),
			'current_user': users.get_current_user(),
			'form': form,
		}
		return context


class BlogManager():
	def published(self):
		entries_qs = Entry.all().order('-date')
		entry_list = []
		for e in entries_qs:
			editable = users.is_current_user_admin() or e.author == users.get_current_user()
			if editable:
				e.id = str(e.key().id())
			entry_list.append({ 'editable': str(editable), 'entry': e })
		return entry_list
	def single(self, slug):
		e = Entry.all().filter('slug =', slug).get()
		editable = users.is_current_user_admin() or e.author == users.get_current_user()
		if editable:
			e.id = str(e.key().id())
		return [{"entry": e, "editable": str(editable)}]
	def post(self):
		pass

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

	objects = BlogManager()
	users = UserManager()

	def own(self, user):
		"""Returns True if 'user' owns the Entry"""
		return self.author == user
	
	def __unicode__(self):
		"""Returns the Entry title"""
		return self.title

	def put(self):
		"""Establish an author for the Entry and an unique slug"""
		if not self.author:
			self.author = users.get_current_user()
		if self.author and self.author != users.get_current_user() and users.is_current_user_admin():
			self.moderated = "moderated"
		if not self.slug:
			self.slug = slugify(self.title, instance=self)
		super(Entry, self).put()

	def is_valid(self, form, request):
		if not form.is_valid():
			messages.add_message(request, messages.ERROR, "Not a valid entry")
			return False
		if not users.get_current_user():
			messages.add_message(request, messages.ERROR, "Must be logged in")
			return False
		if self.author:
			if self.author != users.get_current_user():
				messages.add_message(request, messages.ERROR, "You are not the owner!")
				return False
		return True

