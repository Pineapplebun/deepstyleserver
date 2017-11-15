from django import template

register = template.Library()

@register.filter(name='remove')
def remove(value, substring):
    """Remove a substring from a string """
    return value.replace(substring,"")
