from django import template

register = template.Library()

@register.filter
def int_to_kilogram(value):
    if value >= 1000:
        return '{:,} kg'.format(value/1000).replace(",",".")
    else:
        return '{:,} gram'.format(value).replace(",",".")