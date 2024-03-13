from django import template

register = template.Library()

@register.filter
def break_loop(value):
    raise StopIteration
