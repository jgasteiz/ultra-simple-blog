# -*- coding: utf-8 -*-
from google.appengine.api import users
from google.appengine.ext import db
from django.template.defaultfilters import slugify

class Entry(db.Model):
	author = db.UserProperty()
	title = db.TextProperty()
	slug = db.TextProperty()
	content = db.TextProperty()
	moderated = db.TextProperty(default="")
	date = db.DateTimeProperty(auto_now_add=True)
	
	def own(self, user):
		return self.author == user
	
	def __unicode__(self):
		return self.title

	def put(self):
		if not self.author:
			self.author = users.get_current_user()
		if self.author and self.author != users.get_current_user() and users.is_current_user_admin():
			self.moderated = "moderated"
		key = super(Entry, self).put()
		if not self.slug:
			self.slug = '%i-%s' % (key.id(), slugify(self.title))
		super(Entry, self).put()