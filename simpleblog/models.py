# -*- coding: utf-8 -*-
from google.appengine.ext import db
from django.template.defaultfilters import slugify

class Entry(db.Model):
	author = db.UserProperty()
	title = db.TextProperty()
	slug = db.TextProperty()
	content = db.TextProperty()
	date = db.DateTimeProperty(auto_now_add=True)

	def own(self, user):
		return self.author == user