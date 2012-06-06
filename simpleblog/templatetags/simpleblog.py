import bleach
from django import template

register = template.Library()

@register.filter(name='allowtags')
def allowtags(value):
	return bleach.clean(value, 
		tags=bleach.ALLOWED_TAGS + ['b', 'strong', 'em', 'i', 'iframe'], 
		attributes=bleach.ALLOWED_TAGS + ['width', 'height', 'src', 'frameborder'], 
		strip=True)
	
allowtags.is_safe = True