from django import template

register = template.Library()

@register.filter()
def item(d, key):
    return d.get(key)
