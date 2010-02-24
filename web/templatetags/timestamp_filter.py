from datetime import datetime

from django import template

register = template.Library()

@register.filter
def epoch(value):
    try:
        return datetime.fromtimestamp(value)
    except AttributeError:
        return ''
