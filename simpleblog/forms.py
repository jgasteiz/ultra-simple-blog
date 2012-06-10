# -*- coding: utf-8 -*-
from django import forms

class EntryForm(forms.Form):
	title = forms.CharField(widget = forms.TextInput(attrs={"placeholder": "Title"}))
	content = forms.CharField(widget = forms.Textarea)