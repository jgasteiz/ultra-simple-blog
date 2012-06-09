# -*- coding: utf-8 -*-
from google.appengine.api import users
from google.appengine.ext import db
from simpleblog.utils import uuslug as slugify
import re

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