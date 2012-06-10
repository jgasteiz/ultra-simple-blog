# -*- coding: utf-8 -*-
from google.appengine.api import users
from google.appengine.ext import db
from simpleblog.utils import uuslug as slugify
from simpleblog.forms import EntryForm
from django.contrib import messages

class ContextManager():
	def get_context(self, type):
		# Sets login/logout urls
		if users.get_current_user():
			url = users.create_logout_url('/')
			url_linktext = 'Logout'
			form = EntryForm()
		else:
			url = users.create_login_url('/')
			url_linktext = 'Login'
			form = ''
		if type == 'main':
			blocks =  {'footer': 1}
		elif type == 'single':
			blocks = ''
		elif type == 'author':
			blocks = {'footer': 1}
		context = {
			'url': url,
			'url_linktext': url_linktext,
			'is_admin': users.is_current_user_admin(),
			'current_user': users.get_current_user(),
			'form': form,
			'blocks': blocks
		}
		return context


class BlogManager():
	def published(self):
		return Entry.all().order('-date')
	def single(self, slug):
		return [Entry.all().filter('slug =', slug).get()]
	def author(self, author):
		return Entry.all().filter('author =', users.User(author)).order('-date')

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
