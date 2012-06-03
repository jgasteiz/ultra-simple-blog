from google.appengine.ext import db

class Entry(db.Model):
	author = db.UserProperty()
	title = db.TextProperty()
	slug = db.TextProperty()
	content = db.TextProperty()
	date = db.DateTimeProperty(auto_now_add=True)