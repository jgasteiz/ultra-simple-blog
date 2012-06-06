import bleach
from django import template

register = template.Library()

@register.filter(name='allowtags')
def allowtags(value):
	return bleach.clean(value, 
		tags=['iframe', 'img', 'a', 'abbr', 'acronym', 'b', 'blockquote', 'code', 'em', 'i', 'li', 'ol', 'strong', 'ul'], 
		attributes={'a': ['href', 'title'], 'acronym': ['title'], 'abbr': ['title'], 'img': ['src', 'alt'], 'iframe': ['width', 'height', 'src', 'frameborder']},
		strip=True)
	
allowtags.is_safe = True