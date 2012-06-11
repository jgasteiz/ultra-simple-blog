# -*- coding: utf-8 -*-
from django.http import HttpResponseRedirect

from django.views.generic import ListView, DetailView, View

from simpleblog.models import Entry
from simpleblog.forms import EntryForm

class EntryListView(ListView):
	"""
	Main page. Loads all the entries, ordered by date.
	"""
	paginate_by = 5
	context_object_name = 'entry_list'
	template_name = 'simpleblog/entry_list.html'

	def get_queryset(self):
		return Entry.all().order('-date')

	def get_context_data(self, **kwargs):
		context = super(EntryListView, self).get_context_data(**kwargs)
		context.update(Entry.context.get_context('main'))
		return context

class EntryDetailView(ListView):
	"""
	Single page for an entry
	"""
	context_object_name = 'entry'
	template_name = 'simpleblog/entry_detail.html'

	def get_queryset(self):
		return Entry.all().filter('slug =', self.kwargs['slug']).get()

	def get_context_data(self, **kwargs):
		context = super(EntryDetailView, self).get_context_data(**kwargs)
		context.update(Entry.context.get_context('single'))
		return context

class EntryCreateView(View):
	"""
	Creates an entry
	"""
	def post(self, request, *args, **kwargs):
		e = Entry()
		e.put(EntryForm(request.POST), request)
		return HttpResponseRedirect("/single/" + e.slug)

class EntryEditView(View):
	"""
	Edits an entry
	"""
	def post(self, request, *args, **kwargs):
		e = Entry.get_by_id(int(request.POST['id']))
		if e:
			e.put(EntryForm(request.POST), request)
		return HttpResponseRedirect("/single/" + e.slug)

class EntryDeleteView(View):
	"""
	Deletes an entry
	"""
	def post(self, request, *args, **kwargs):
		e = Entry.get_by_id(int(request.POST['id']))
		if e:
			e.delete(request)
		return HttpResponseRedirect("/")

class AuthorListView(ListView):
	"""
	Loads author entries ordered by date.
	CURRENTLY NOT IN USE
	"""
	paginate_by = 5
	context_object_name = 'entry_list'
	template_name = 'simpleblog/entry_list.html'

	def get_queryset(self):
		return Entry.objects.author(self.kwargs['author'])

	def get_context_data(self, **kwargs):
		context = super(AuthorListView, self).get_context_data(**kwargs)
		context.update(Entry.context.get_context('main'))
		return context
