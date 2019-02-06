from django import template

register = template.Library()

@register.filter
def int_to_rupiah(value):
    return 'Rp. '+ '{:,}'.format(value).replace(",",".") + ',-'
