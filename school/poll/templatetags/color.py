from django import template
from poll.models import *

register = template.Library()


@register.filter(name='color')
def color(group):
    color_class = {'ADMIN': 'bg-secondary', 'CP': 'bg-primary', 'CE1': 'bg-warning', 'CE2': 'bg-danger', 'CM1': 'bg-danger', 'CM2': 'bg-light'}
    color = color_class[group]
    return color
