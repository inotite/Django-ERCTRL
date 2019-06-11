from django import template
register = template.Library()


@register.filter(name='times')
def times(number):
    try:
        return range(number)
    except TypeError:
        return []
