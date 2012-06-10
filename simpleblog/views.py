# -*- coding: utf-8 -*-
from django.http import HttpResponseRedirect

from django.views.generic import ListView

from simpleblog.models import Entry
from simpleblog.forms import EntryForm

class BlogView(ListView):
	"""
	Main page. Loads all the entries, ordered by date.
	If request method is post, there may be creating or editing an entry.
	"""
	paginate_by = 5
	context_object_name = 'entry_list'
	template_name = 'simpleblog/index.html'

	def get_queryset(self):
		return Entry.objects.published()

	def post(self, request, *args, **kwargs):
		"""
		If everything's correct, creates/edits/deletes an entry
		"""
		if request.POST['type'] == 'create':
			e = Entry()
			e.put(EntryForm(request.POST), request)

		elif request.POST['type'] == 'edit':
			e = Entry.get_by_id(int(request.POST['id']))
			if e:
				e.put(EntryForm(request.POST), request)

		elif request.POST['type'] == 'delete':
			e = Entry.get_by_id(int(request.POST['id']))
			if e:
				e.delete(request)
			return HttpResponseRedirect("/")

		return HttpResponseRedirect("/" + e.slug)

	def get_context_data(self, **kwargs):
		context = super(BlogView, self).get_context_data(**kwargs)
		context.update(Entry.context.get_context('main'))
		return context


class PostView(ListView):
	"""
	Single page for an entry
	"""
	context_object_name = 'entry_list'
	template_name = 'simpleblog/index.html'

	def get_queryset(self):
		return Entry.objects.single(self.kwargs['slug'])

	def get_context_data(self, **kwargs):
		context = super(PostView, self).get_context_data(**kwargs)
		context.update(Entry.context.get_context('single'))
		return context

class AuthorView(ListView):
	"""
	Author's posts
	"""
	context_object_name = 'entry_list'
	template_name = 'simpleblog/index.html'

	def get_queryset(self):
		return Entry.objects.author(self.kwargs['author'])

	def get_context_data(self, **kwargs):
		context = super(AuthorView, self).get_context_data(**kwargs)
		context.update(Entry.context.get_context('author'))
		return context



